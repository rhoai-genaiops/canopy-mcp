// src/components/Day.js
import React from 'react';
import './Day.css';

const Day = ({ day, schedules, onEventClick, currentMonth, currentYear }) => {
  const today = new Date();
  const isToday = today.getDate() === day && 
                  today.getMonth() === currentMonth && 
                  today.getFullYear() === currentYear;
  const hasEvents = schedules.length > 0;

  const getCategoryClass = (category) => {
    return category.toLowerCase().replace(/\s+/g, '-');
  };

  const getCategoryEmoji = (category) => {
    const emojiMap = {
      'Lecture': '📚',
      'Lab': '🔬',
      'Meeting': '👥',
      'Office Hours': '🕐',
      'Assignment': '📝',
      'Defense': '🎓',
      'Workshop': '🛠️',
      'Study Group': '👨‍🎓',
      'Seminar': '🎤',
      'Grading': '📊',
      'Advising': '💬'
    };
    return emojiMap[category] || '📅';
  };

  const formatTime = (timeString) => {
    return new Date(timeString).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: true 
    });
  };

  const getStatusColor = (status) => {
    if (status >= 1.0) return '#4caf50'; // Completed - Green
    if (status >= 0.5) return '#ff9800'; // In Progress - Orange  
    return '#2196f3'; // Not Started - Blue
  };

  return (
    <div className={`day ${isToday ? 'today' : ''} ${hasEvents ? 'has-events' : ''}`}>
      <div className="day-number">
        {day}
        {hasEvents && <div className="event-count">{schedules.length}</div>}
      </div>
      
      <div className="schedule-list">
        {schedules.length > 0 ? (
          schedules.map((schedule) => (
            <div 
              key={schedule.sid} 
              className={`schedule-item ${getCategoryClass(schedule.category)}`}
              style={{ borderLeftColor: getStatusColor(schedule.status) }}
              onClick={() => onEventClick(schedule)}
              title="Click to view details"
            >
              <div className="schedule-name">
                {getCategoryEmoji(schedule.category)} {schedule.name}
              </div>
              
              <div className="schedule-time">
                {formatTime(schedule.start_time)} - {formatTime(schedule.end_time)}
              </div>
              
              {schedule.content && (
                <div className="schedule-content">
                  {schedule.content}
                </div>
              )}
              
              <div className={`priority-indicator priority-${schedule.level}`}></div>
              <div className="click-indicator">👁️</div>
            </div>
          ))
        ) : (
          <div className="no-schedule">No events</div>
        )}
      </div>
    </div>
  );
};

export default Day;
