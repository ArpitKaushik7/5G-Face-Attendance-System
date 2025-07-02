import React, { useEffect, useState } from 'react';
import API from '../services/api';

function AttendanceTable() {
  const [attendance, setAttendance] = useState([]);

  useEffect(() => {
    API.get('/attendance/')
      .then((res) => setAttendance(res.data.attendance))
      .catch((err) => console.error("Error fetching attendance:", err));
  }, []);

  return (
    <div>
      <h2>Attendance Logs</h2>
      <table border="1">
        <thead>
          <tr>
            <th>ID</th><th>Name</th><th>Branch</th><th>Batch</th>
            <th>Subject</th><th>Lecture Slot</th><th>Date</th><th>Time</th>
          </tr>
        </thead>
        <tbody>
          {attendance.map((entry, idx) => (
            <tr key={idx}>
              <td>{entry.id}</td>
              <td>{entry.name}</td>
              <td>{entry.branch}</td>
              <td>{entry.batch}</td>
              <td>{entry.subject}</td>
              <td>{entry.lecture_slot}</td>
              <td>{entry.date}</td>
              <td>{entry.time}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AttendanceTable;
