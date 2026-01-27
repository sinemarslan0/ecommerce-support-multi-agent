// Configuration
const API_BASE_URL = 'https://ecommerce-support-multi-agent.onrender.com/';
let conversationId = null;
let isProcessing = false;

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const typingIndicator = document.getElementById('typingIndicator');

// Initialize chat
document.addEventListener('DOMContentLoaded', () => {
    initializeChat();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    chatForm.addEventListener('submit', handleSubmit);
    
    // Auto-resize input (optional enhancement)
    messageInput.addEventListener('input', () => {
        messageInput.style.height = 'auto';
        messageInput.style.height = messageInput.scrollHeight + 'px';
    });
}

// Initialize chat session
async function initializeChat() {
    try {
        // Generate a unique conversation ID
        conversationId = generateConversationId();
        console.log('Chat initialized with conversation ID:', conversationId);
    } catch (error) {
        console.error('Error initializing chat:', error);
        showError('Failed to initialize chat. Please refresh the page.');
    }
}

// Handle form submission
async function handleSubmit(e) {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    if (!message || isProcessing) return;
    
    // Clear input and disable sending
    messageInput.value = '';
    messageInput.style.height = 'auto';
    isProcessing = true;
    updateSendButton(true);
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Show typing indicator
    typingIndicator.style.display = 'flex';
    
    try {
        // Send message to backend
        const response = await sendMessage(message);
        
        // Hide typing indicator
        typingIndicator.style.display = 'none';
        
        // Add bot response to chat
        if (response && response.response) {
            addMessage(response.response, 'bot');
        } else {
            throw new Error('Invalid response from server');
        }
    } catch (error) {
        console.error('Error sending message:', error);
        typingIndicator.style.display = 'none';
        showError('Failed to send message. Please try again.');
    } finally {
        isProcessing = false;
        updateSendButton(false);
        messageInput.focus();
    }
}

// Send message to backend
async function sendMessage(message) {
    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                conversation_id: conversationId,
            }),
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error in sendMessage:', error);
        throw error;
    }
}

// Add message to chat UI
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const avatarDiv = document.createElement('div');
    avatarDiv.className = `message-avatar ${sender}-avatar`;
    
    if (sender === 'bot') {
        avatarDiv.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
            </svg>
        `;
    } else {
        avatarDiv.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
            </svg>
        `;
    }
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const textP = document.createElement('p');
    textP.textContent = text;
    
    const timeSpan = document.createElement('span');
    timeSpan.className = 'message-time';
    timeSpan.textContent = formatTime(new Date());
    
    contentDiv.appendChild(textP);
    contentDiv.appendChild(timeSpan);
    
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    scrollToBottom();
}

// Show error message
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        <span>${message}</span>
    `;
    
    const inputContainer = document.querySelector('.chat-input-container');
    inputContainer.insertBefore(errorDiv, inputContainer.firstChild);
    
    // Remove error after 5 seconds
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Update send button state
function updateSendButton(disabled) {
    sendBtn.disabled = disabled;
}

// Scroll chat to bottom
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Format time
function formatTime(date) {
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}

// Generate unique conversation ID
function generateConversationId() {
    return `conv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

// Export functions for potential future use
window.chatApp = {
    sendMessage,
    addMessage,
    showError,
};

