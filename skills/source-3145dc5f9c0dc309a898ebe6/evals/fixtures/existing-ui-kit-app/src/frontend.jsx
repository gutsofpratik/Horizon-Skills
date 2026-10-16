import React, { useEffect, useState } from 'react';
import ForgeReconciler, { Text } from '@forge/react';
import { invoke } from '@forge/bridge';

const App = () => {
  const [summary, setSummary] = useState('Loading');
  useEffect(() => {
    invoke('get-summary').then(setSummary);
  }, []);
  return <Text>{summary}</Text>;
};

ForgeReconciler.render(<App />);
