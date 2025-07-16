import React, { useEffect, useState } from "react";
import axios from "axios";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from "@mui/material";

interface Operator {
  userid: string;
  fullusername: string;
  location: string;
  mobileno: string;
  aadharcard: string;
}

const Operators: React.FC = () => {
  const [operators, setOperators] = useState<Operator[]>([]);

  useEffect(() => {
    const fetchOperators = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/users");
        setOperators(response.data);
      } catch (error) {
        console.error("Error fetching operators:", error);
      }
    };

    fetchOperators();
  }, []);

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>User ID</TableCell>
            <TableCell>Full Name</TableCell>
            <TableCell>Location</TableCell>
            <TableCell>Mobile</TableCell>
            <TableCell>Aadhar</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {operators.map((operator) => (
            <TableRow key={operator.userid}>
              <TableCell>{operator.userid}</TableCell>
              <TableCell>{operator.fullusername}</TableCell>
              <TableCell>{operator.location}</TableCell>
              <TableCell>{operator.mobileno}</TableCell>
              <TableCell>{operator.aadharcard}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default Operators;
