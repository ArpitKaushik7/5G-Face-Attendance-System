import React from 'react';
import AttendanceTable from 'E:/5G Face Attendance System/frontend/dashboard/src/components/attendanceTable.js';
import StudentForm from 'E:/5G Face Attendance System/frontend/dashboard/src/components/studentForm.js';
import StudentSearch from 'E:/5G Face Attendance System/frontend/dashboard/src/components/studentSearch.js';

function App() {
  return (
    <div className="App">
      <h1>5G Face Attendance Dashboard</h1>
      <StudentForm />
      <hr />
      <AttendanceTable />
      <hr />
      <StudentSearch />
    </div>
  );
}

export default App;
