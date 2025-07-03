// src/components/Calendar.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Day from './Day';
import EventModal from './EventModal';
import './Calendar.css';

const Calendar = () => {
  const [schedules, setSchedules] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [currentMonth, setCurrentMonth] = useState(new Date().getMonth());
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [showEventModal, setShowEventModal] = useState(false);
  const [newSchedule, setNewSchedule] = useState({
    sid: "",
    name: "",
    content: "",
    category: "Lecture",
    level: 1,
    status: 0.0,
    creation_time: "",
    start_time: "",
    end_time: ""
  });

  // Fetch schedules when the component mounts or the month changes
  useEffect(() => {
    fetchSchedules();
  }, [currentMonth]);

  // Function to fetch schedules from the backend
  const fetchSchedules = () => {
    axios.get('http://127.0.0.1:8000/schedules')
      .then((response) => {
        setSchedules(response.data);
      })
      .catch((error) => {
        console.error('Error fetching schedules:', error);
      });
  };

  // Handle month navigation
  const handleMonthChange = (increment) => {
    setCurrentMonth((prev) => (prev + increment + 12) % 12);
  };

  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewSchedule((prev) => ({ ...prev, [name]: value }));
  };

  // Handle form submission
  const handleFormSubmit = async (e) => {
    e.preventDefault();

    // Automatically set the creation_time and generate a unique sid
    const currentDateTime = new Date().toISOString().slice(0, 19).replace('T', ' ');
    const uniqueSid = `${Date.now()}`; // Use the current timestamp as a unique ID

    // Prepare the schedule data with correct types
    const formattedSchedule = {
      ...newSchedule,
      sid: uniqueSid,
      creation_time: currentDateTime,
      status: parseFloat(newSchedule.status),
      level: parseInt(newSchedule.level),
    };

    try {
      const response = await axios.post('http://127.0.0.1:8000/schedules', formattedSchedule, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      setSchedules([...schedules, response.data]);
      setShowForm(false);
    } catch (error) {
      console.error('Error creating schedule:', error.response?.data || error.message);
    }
  };

  // Handle event click to open modal
  const handleEventClick = (event) => {
    setSelectedEvent(event);
    setShowEventModal(true);
  };

  // Close event modal
  const closeEventModal = () => {
    setShowEventModal(false);
    setSelectedEvent(null);
  };

  // Calculate the number of days in the current month
  const daysInMonth = new Date(2024, currentMonth + 1, 0).getDate();
  const daysArray = Array.from({ length: daysInMonth }, (_, i) => i + 1);

  return (
    <div className="calendar-container">
      <div className="month-navigation">
        <button onClick={() => handleMonthChange(-1)}>← Previous</button>
        <span>{new Date(2024, currentMonth).toLocaleString("default", { month: "long", year: "numeric" })}</span>
        <button onClick={() => handleMonthChange(1)}>Next →</button>
      </div>

      <button className="add-schedule-btn" onClick={() => setShowForm(!showForm)}>
        {showForm ? "✕ Close Form" : "+ Add New Event"}
      </button>

      {/* Schedule creation form */}
      {showForm && (
        <form onSubmit={handleFormSubmit} className="schedule-form">
          <h3>📅 Create New Event</h3>
          
          <div className="form-group">
            <label>Event Name</label>
            <input 
              type="text" 
              name="name" 
              placeholder="e.g., CS 301: Machine Learning Lecture"
              onChange={handleInputChange} 
              required 
            />
          </div>

          <div className="form-group">
            <label>Description</label>
            <textarea 
              name="content" 
              placeholder="Event details, location, notes..."
              onChange={handleInputChange}
              rows="3"
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Category</label>
              <select name="category" onChange={handleInputChange} value={newSchedule.category}>
                <option value="Lecture">📚 Lecture</option>
                <option value="Lab">🔬 Lab</option>
                <option value="Meeting">👥 Meeting</option>
                <option value="Office Hours">🕐 Office Hours</option>
                <option value="Assignment">📝 Assignment</option>
                <option value="Defense">🎓 Defense</option>
                <option value="Workshop">🛠️ Workshop</option>
                <option value="Study Group">👨‍🎓 Study Group</option>
                <option value="Seminar">🎤 Seminar</option>
                <option value="Grading">📊 Grading</option>
                <option value="Advising">💬 Advising</option>
              </select>
            </div>

            <div className="form-group">
              <label>Priority Level</label>
              <select name="level" onChange={handleInputChange} value={newSchedule.level}>
                <option value="1">🟢 Low Priority</option>
                <option value="2">🟡 Medium Priority</option>
                <option value="3">🔴 High Priority</option>
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Start Time</label>
              <input type="datetime-local" name="start_time" onChange={handleInputChange} required />
            </div>

            <div className="form-group">
              <label>End Time</label>
              <input type="datetime-local" name="end_time" onChange={handleInputChange} required />
            </div>
          </div>

          <button type="submit" className="submit-btn">✨ Create Event</button>
        </form>
      )}

      {/* Calendar header with day names */}
      <div className="calendar-header">
        <div className="calendar-header-day">Sun</div>
        <div className="calendar-header-day">Mon</div>
        <div className="calendar-header-day">Tue</div>
        <div className="calendar-header-day">Wed</div>
        <div className="calendar-header-day">Thu</div>
        <div className="calendar-header-day">Fri</div>
        <div className="calendar-header-day">Sat</div>
      </div>

      {/* Display the calendar */}
      <div className="calendar">
        {daysArray.map((day) => (
          <Day 
            key={day} 
            day={day} 
            schedules={schedules.filter(schedule => {
              const scheduleDate = new Date(schedule.start_time);
              return (
                scheduleDate.getDate() === day &&
                scheduleDate.getMonth() === currentMonth
              );
            })}
            onEventClick={handleEventClick}
          />
        ))}
      </div>

      {/* Event Details Modal */}
      <EventModal 
        event={selectedEvent}
        isOpen={showEventModal}
        onClose={closeEventModal}
      />
    </div>
  );
};

export default Calendar;
