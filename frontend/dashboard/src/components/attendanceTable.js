import React, { useEffect, useState } from 'react';
import axios from 'axios';

const AttendanceTable = () => {
  const [attendance, setAttendance] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/attendance/')
      .then(response => {
        setAttendance(response.data.attendance);
      })
      .catch(error => {
        console.error('Error fetching attendance:', error);
      });
  }, []);

  return (
    <div>
      <h2>Recent Attendance</h2>
      <table border="1" cellPadding="6">
        <thead>
          <tr>
            <th>ID</th>
            <th>Subject</th>
            <th>Lecture Slot</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {attendance.map((entry, index) => (
            <tr key={index}>
              <td>{entry.id}</td>
              <td>{entry.subject}</td>
              <td>{entry.lecture_slot}</td>
              <td>{new Date(entry.time).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AttendanceTable;
