/**
 * <pendo-poll> — Headless custom element for poll data storage.
 *
 * Declares a single poll field and stores its value. Renders nothing.
 * Used by the inline `actions` factory to collect and submit poll responses.
 *
 * Attributes:
 *   poll-id (required) — format: cb-{Type}-{shortRandom}
 *   type    (required) — data type being collected:
 *     NumberScale   — integer (ratings, scales)
 *     FreeForm      — string (open text)
 *     SingleChoice  — string (one selected option label)
 *     MultiSelect   — array of strings (multiple selections, serialized as JSON)
 *     Boolean       — true/false (stored as 1/0)
 *     Ranking       — ordered array (serialized as JSON)
 *
 * Methods:
 *   .setValue(value)    — stores the current value (native JS type)
 *   .getValue()        — returns the stored value (native JS type)
 *   .getSerializedValue() — returns the value serialized for step.response()
 *   .backendType        — the Pendo backend poll type this maps to
 */

var BACKEND_TYPE_MAP = {
    NumberScale: 'NumberScale',
    FreeForm: 'FreeForm',
    SingleChoice: 'FreeForm',
    MultiSelect: 'FreeForm',
    Boolean: 'NumberScale',
    Ranking: 'FreeForm'
};

class PendoPoll extends HTMLElement {
    connectedCallback() {
        this.style.display = 'none';
        this._value = undefined;
    }

    get pollId() {
        return this.getAttribute('poll-id');
    }

    get type() {
        return this.getAttribute('type');
    }

    get backendType() {
        return BACKEND_TYPE_MAP[this.type] || 'FreeForm';
    }

    setValue(value) {
        this._value = value;
        this.dispatchEvent(new CustomEvent('pendo-poll-change', {
            detail: { pollId: this.pollId, value: value, type: this.type },
            bubbles: true
        }));
    }

    getValue() {
        return this._value;
    }

    getSerializedValue() {
        var v = this._value;
        if (v === undefined || v === null) return undefined;

        switch (this.type) {
        case 'NumberScale':
            return typeof v === 'number' ? v : parseInt(v, 10);
        case 'Boolean':
            return v ? 1 : 0;
        case 'MultiSelect':
        case 'Ranking':
            return Array.isArray(v) ? JSON.stringify(v) : String(v);
        case 'SingleChoice':
        case 'FreeForm':
        default:
            return String(v);
        }
    }

    hasValue() {
        if (this._value === undefined || this._value === null) return false;
        if (this.type === 'MultiSelect' || this.type === 'Ranking') {
            return Array.isArray(this._value) && this._value.length > 0;
        }
        return this._value !== '';
    }
}

export { PendoPoll, BACKEND_TYPE_MAP };
