# zoo.py — Class Hierarchy

## Use these, don't replace these

**Framework-first**: FiftyOne already provides the pickle-safe primitives. Subclassing or overriding these re-introduces the **Worker-pickle constraint** failures (see DATALOADER.md).

| Concern | Use this | Do NOT |
|---------|----------|--------|
| Batch collation | `TorchModelMixin.collate_fn` (inherited) | Override `collate_fn` |
| Dataset item loading | `fiftyone.utils.torch.ImageGetItem(raw_inputs=True)` | Subclass `GetItem` |
| `transforms` / `preprocess` / `ragged_batches` / `needs_fields` / `has_collate_fn` | Implement on your model class | These are the seams — implement, don't avoid |

## Config

```python
import fiftyone.utils.torch as fout

class MyModelConfig(fout.TorchImageModelConfig):
    def __init__(self, d: dict):
        if "raw_inputs" not in d:
            d["raw_inputs"] = True
        super().__init__(d)
        self.model_path = self.parse_string(d, "model_path", default="org/model")
```

## Model — multi-inheritance order matters

```python
import fiftyone.core.models as fom
from fiftyone.core.models import SupportsGetItem, TorchModelMixin
from fiftyone.utils.torch import ImageGetItem

class MyBaseModel(fom.Model, fom.SamplesMixin, SupportsGetItem, TorchModelMixin):
    def __init__(self, config):
        fom.SamplesMixin.__init__(self)
        SupportsGetItem.__init__(self)
        self._preprocess = False
        self.config = config

    @property
    def transforms(self): return None

    @property
    def preprocess(self) -> bool: return self._preprocess
    @preprocess.setter
    def preprocess(self, value: bool): self._preprocess = value

    @property
    def ragged_batches(self) -> bool: return False

    @property
    def needs_fields(self) -> dict: return self._fields
    @needs_fields.setter
    def needs_fields(self, fields: dict): self._fields = fields

    @property
    def has_collate_fn(self) -> bool: return True

    def build_get_item(self, field_mapping=None) -> ImageGetItem:
        return ImageGetItem(field_mapping=field_mapping, raw_inputs=True)
```

## predict / predict_all — input dispatch

`dataset.apply_model` always passes `PIL.Image` to `predict_all`. The framework loads the image from `sample.filepath` before calling the model, so do **not** add an `isinstance(_, str)` branch — it is dead code. The accepted input types are documented on the public contracts `fiftyone.core.models.Model.predict_all` (numpy HWC / NHWC) and `fiftyone.utils.torch.TorchImageModel.predict_all` (PIL / numpy / Torch tensor); neither lists `str`.

For non-VLM models, accept the image directly:

```python
def predict(self, arg, sample=None):
    return self.predict_all([arg], samples=[sample] if sample else None)[0]

def predict_all(self, batch, samples=None):
    return [self._run_inference(image) for image in batch]
```

**VLM exception — optional `dict` input.** For VLMs you often want per-item prompts. `apply_model` does not produce dicts either (the DataLoader still yields `PIL.Image`), so a dict shape is purely a *direct-invocation convenience* for users calling `model.predict({"image": img, "prompt": "..."})` outside the framework. If you want to expose that, branch on `isinstance(item, dict)` and fall through otherwise:

```python
def predict_all(self, batch, samples=None):
    results = []
    for i, item in enumerate(batch):
        sample = samples[i] if samples and i < len(samples) else None
        if isinstance(item, dict):
            image = item.get("image") or item.get("filepath")
            prompt = item.get("prompt")
        else:
            image, prompt = item, None     # PIL.Image (DataLoader path)

        if prompt is None and sample and "prompt_field" in self._fields:
            fn = self._fields["prompt_field"]
            if sample.has_field(fn):
                prompt = sample.get_field(fn)
        prompt = prompt or self.config.prompt
        results.append(self._run_inference(image, prompt))
    return results
```

If you don't want the dict convenience, drop the `isinstance` check entirely and assume `PIL.Image`.

## Runtime parameters as setters

Every parameter a user might change between calls should be a `@property` + `@<name>.setter` on the model class — not a construction-only argument. Without this, users must reconstruct the model to change anything, which reloads the (often multi-GB) weights on the next inference call.

### The heuristic

If the parameter is passed to `self._model(...)`, `self._model.generate(...)`, or any post-processing step the model class applies to the raw output, it is a *runtime parameter* and should be a setter. If it changes what gets loaded (weight file, dtype, device, architecture variant), it is *construction-only* and reload is unavoidable.

| Category | Setter? |
|---|---|
| Model identity (`model_path`, architecture variant) | No |
| Precision / placement (`torch_dtype`, `device`) | No |
| Per-call inputs that build the forward call (prompts, class lists, schemas, tool definitions) | Yes |
| Generation / decoding params (`max_new_tokens`, `temperature`, `do_sample`, `top_p`, `top_k`, `repetition_penalty`, beam width, ...) | Yes |
| Operation / task / mode selectors that pick a prompt template or post-processor | Yes (validate against the allowed set) |
| Post-processing thresholds (`confidence_threshold`, `iou_threshold`, `max_detections`) | Yes |
| Framework contracts (`transforms`, `ragged_batches`, `has_collate_fn`, `build_get_item`, `collate_fn`) | No — fixed by contract |
| `media_type` | No when fixed by a leaf class; Yes when one class handles both |

### Pattern

Pick one storage location and use it consistently across the project — `self.config.X` matches most FiftyOne reference integrations; `self._X` matches some others. Internal code (`predict_all`, `_run_inference`, `_generate`, etc.) reads from that storage directly. **Setters are an external API only**; do not call `self.X = value` from your own helpers — it adds confusion without benefit.

```python
@property
def operation(self) -> str:
    return self.config.operation

@operation.setter
def operation(self, value: str) -> None:
    if value not in VALID_OPERATIONS:
        raise ValueError(
            f"Invalid operation '{value}'. "
            f"Must be one of {sorted(VALID_OPERATIONS)}"
        )
    self.config.operation = value
```

Validating setters re-use the same check that `Config.__init__` performs — extract a module-level `VALID_X` constant so both sites share one source of truth and cannot drift. Pass-through setters assign the value as-is; **do not wrap with `int()` / `float()` / `bool()` coercions**. Silent coercion has surprising edges (`bool("False")` is `True`, `int("8")` accepts strings, `int(8.9)` truncates); let the user supply the right type and fail loudly on real mistakes.

Weights survive any number of setter mutations because the only thing changing is a field on `self.config` (or `self._X`); `self._model` is untouched. Reloading is required only when one of the construction-only parameters changes.
