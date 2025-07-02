import React, { useState } from 'react';
import API from '../services/api';

function StudentForm() {
  const [formData, setFormData] = useState({
    id: '', name: '', branch: '', batch: ''
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await API.post('/addStudents', formData);
      alert('Student added successfully');
    } catch (err) {
      console.error('Add student error:', err);
      alert('Error adding student');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Add Student</h2>
      <input name="id" placeholder="ID" onChange={handleChange} required />
      <input name="name" placeholder="Name" onChange={handleChange} required />
      <input name="branch" placeholder="Branch" onChange={handleChange} required />
      <input name="batch" placeholder="Batch" onChange={handleChange} required />
      <button type="submit">Add</button>
    </form>
  );
}

export default StudentForm;
