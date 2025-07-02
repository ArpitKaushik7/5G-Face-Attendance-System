import React from 'react';
import AttendanceTable from 'E:/5G Face Attendance System/frontend/dashboard/src/components/attendanceTable.js';
import StudentForm from 'E:/5G Face Attendance System/frontend/dashboard/src/components/studentForm.js';
import StudentSearch from 'E:/5G Face Attendance System/frontend/dashboard/src/components/studentSearch.js';

function App() {
  return (
    <div style={{ padding: 20 }}>
      <h1>5G Face Attendance Dashboard</h1>
      <StudentForm />
      <hr />
      <StudentSearch />
      <hr />
      <AttendanceTable />
    </div>
  );
}

export default App;
