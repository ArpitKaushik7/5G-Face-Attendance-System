import React, { useEffect, useState } from 'react';
import axios from 'axios';

const AttendanceTable = () => {
  const [attendance, setAttendance] = useState([]);

  useEffect(() => {
    // Make sure your backend server is running on localhost:8000
    axios.get('http://localhost:8000/attendance/')
      .then(response => {
        // The API returns the data inside a key called 'attendance'
        setAttendance(response.data.attendance);
      })
      .catch(error => {
        console.error('Error fetching attendance:', error);
      });
  }, []); // The empty array ensures this effect runs only once

  return (
    <div>
      <h2>Recent Attendance</h2>
      <table border="1" cellPadding="6">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Subject</th>
            <th>Lecture Slot</th>
            <th>Time</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {/* Use .map() to iterate over the attendance array */}
          {attendance.map((entry, index) => {
            // Combine date and time to create a full datetime string
            // The 'T' is a standard separator for ISO 8601 format
            const combinedDateTimeString = `${entry.date}T${entry.time}`;
            
            // Create a new Date object from the combined string
            const formattedDateTime = new Date(combinedDateTimeString);

            // Check if the Date object is valid before rendering
            const isDateValid = !isNaN(formattedDateTime);

            return (
              <tr key={index}>
                <td>{entry.id}</td>
                <td>{entry.name}</td>
                <td>{entry.subject}</td>
                <td>{entry.lecture_slot}</td>
                {/* Check if date is valid, then format for display */}
                <td>{isDateValid ? formattedDateTime.toLocaleTimeString() : 'Invalid Time'}</td>
                <td>{isDateValid ? formattedDateTime.toLocaleDateString() : 'Invalid Date'}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default AttendanceTable;