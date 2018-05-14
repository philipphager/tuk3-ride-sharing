import React from 'react';
import ResizableMap from './Map';

const App = () => {
  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <h2 id="heading">Ride Sharing Prototype</h2>
      <ResizableMap />
    </div>
  );
};

export default App;
