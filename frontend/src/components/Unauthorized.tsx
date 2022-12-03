import React from 'react';
import { Callout, Button } from '@blueprintjs/core';
import { useNavigate } from 'react-router-dom';

const Unauthorized = () => {
  const navigate = useNavigate();

  const goBack = () => navigate(-1);

  return (
    <section>
      <Callout intent="danger" title="Unauthorized">
        <p>You do not have access rights</p>
        <div className="flexGrow">
          <Button onClick={goBack}>Go back</Button>
        </div>
      </Callout>
    </section>
  );
};

export default Unauthorized;
