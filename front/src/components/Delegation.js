import React, { useState, useEffect } from "react";
import axios from "axios";

const Delegation = () => {
  const [delegationData, setDelegationData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5001/request_delegation"
        );
        setDelegationData(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
        setDelegationData(null);
      }
    };

    fetchData();
  }, []);

  return (
    <>
      <div style={{ textAlign: "center" }}>
        <h1>Delegation</h1>
        <p>Results for task 1</p>
      </div>
      <pre>{JSON.stringify(delegationData, null, 2)}</pre>
    </>
  );
};

export default Delegation;
