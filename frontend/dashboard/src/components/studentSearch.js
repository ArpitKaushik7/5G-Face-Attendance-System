import React, { useState } from 'react';
import API from '../services/api';

function StudentSearch() {
  const [id, setId] = useState('');
  const [student, setStudent] = useState(null);

  const searchStudent = async () => {
    try {
      const res = await API.get(`/attendance/${id}`);
      setStudent(res.data);
    } catch {
      alert("Student not found");
      setStudent(null);
    }
  };

  return (
    <div>
      <h2>Search Student by ID</h2>
      <input value={id} onChange={(e) => setId(e.target.value)} placeholder="Enter ID" />
      <button onClick={searchStudent}>Search</button>
      {student && (
        <div>
          <p><strong>Name:</strong> {student.name}</p>
          <p><strong>Branch:</strong> {student.branch}</p>
          <p><strong>Batch:</strong> {student.batch}</p>
        </div>
      )}
    </div>
  );
}

export default StudentSearch;
