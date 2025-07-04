// src/components/EventModal.js
import React from 'react';
import './EventModal.css';

const EventModal = ({ event, isOpen, onClose, onDelete }) => {
  if (!isOpen || !event) return null;

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

  const formatDateTime = (dateTimeString) => {
    const date = new Date(dateTimeString);
    return {
      date: date.toLocaleDateString('en-US', { 
        weekday: 'long',
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      }),
      time: date.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: true 
      })
    };
  };

  const getPriorityText = (level) => {
    const priorities = {
      1: { text: 'Low Priority', color: '#4caf50', emoji: '🟢' },
      2: { text: 'Medium Priority', color: '#ff9800', emoji: '🟡' },
      3: { text: 'High Priority', color: '#f44336', emoji: '🔴' }
    };
    return priorities[level] || priorities[1];
  };

  const getStatusText = (status) => {
    if (status >= 1.0) return { text: 'Completed', color: '#4caf50', emoji: '✅' };
    if (status >= 0.5) return { text: 'In Progress', color: '#ff9800', emoji: '⏳' };
    return { text: 'Not Started', color: '#2196f3', emoji: '🔄' };
  };

  const startDateTime = formatDateTime(event.start_time);
  const endDateTime = formatDateTime(event.end_time);
  const priority = getPriorityText(event.level);
  const status = getStatusText(event.status);

  const calculateDuration = () => {
    const start = new Date(event.start_time);
    const end = new Date(event.end_time);
    const diffMs = end - start;
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffMins = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
    
    if (diffHours > 0) {
      return `${diffHours}h ${diffMins > 0 ? diffMins + 'm' : ''}`;
    }
    return `${diffMins}m`;
  };

  const handleDeleteClick = () => {
    if (onDelete && event.sid) {
      onDelete(event.sid);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="event-title">
            <span className="category-emoji">{getCategoryEmoji(event.category)}</span>
            <h2>{event.name}</h2>
          </div>
          <button className="close-button" onClick={onClose}>✕</button>
        </div>

        <div className="modal-body">
          <div className="event-meta">
            <div className="meta-item">
              <span className="meta-label">Category</span>
              <span className="meta-value category-badge">{event.category}</span>
            </div>
            
            <div className="meta-item">
              <span className="meta-label">Priority</span>
              <span className="meta-value priority-badge" style={{ color: priority.color }}>
                {priority.emoji} {priority.text}
              </span>
            </div>
            
            <div className="meta-item">
              <span className="meta-label">Status</span>
              <span className="meta-value status-badge" style={{ color: status.color }}>
                {status.emoji} {status.text}
              </span>
            </div>
            
            <div className="meta-item">
              <span className="meta-label">Duration</span>
              <span className="meta-value">🕐 {calculateDuration()}</span>
            </div>
          </div>

          <div className="event-schedule">
            <h3>📅 Schedule</h3>
            <div className="schedule-details">
              <div className="schedule-item">
                <div className="schedule-label">Start</div>
                <div className="schedule-value">
                  <div className="schedule-date">{startDateTime.date}</div>
                  <div className="schedule-time">{startDateTime.time}</div>
                </div>
              </div>
              
              <div className="schedule-divider">→</div>
              
              <div className="schedule-item">
                <div className="schedule-label">End</div>
                <div className="schedule-value">
                  <div className="schedule-date">{endDateTime.date}</div>
                  <div className="schedule-time">{endDateTime.time}</div>
                </div>
              </div>
            </div>
          </div>

          {event.content && (
            <div className="event-description">
              <h3>📝 Description</h3>
              <p>{event.content}</p>
            </div>
          )}

          <div className="event-id">
            <small>Event ID: {event.sid}</small>
          </div>
        </div>

        <div className="modal-footer">
          <div className="modal-footer-left">
            {onDelete && (
              <button className="btn-danger" onClick={handleDeleteClick}>
                🗑️ Delete Event
              </button>
            )}
          </div>
          <div className="modal-footer-right">
            <button className="btn-secondary" onClick={onClose}>Close</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EventModal;