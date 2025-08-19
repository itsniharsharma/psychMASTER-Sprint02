// Mock data for chat functionality - will be replaced with actual LangChain backend integration

export const mockChatResponses = [
  {
    trigger: ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
    responses: [
      "Hello! I'm psychMASTER, your AI companion for mental health support. How are you feeling today?",
      "Hi there! Welcome to psychMASTER. I'm here to listen and support you. What's on your mind?",
      "Hello! It's great to connect with you. How can I help you with your mental wellness journey today?"
    ]
  },
  {
    trigger: ["stressed", "stress", "overwhelmed", "pressure", "anxious", "anxiety"],
    responses: [
      "I understand you're feeling stressed. That's completely valid. Can you tell me more about what's contributing to these feelings?",
      "Stress can feel overwhelming, but you're not alone in this. Let's explore some coping strategies together. What usually helps you relax?",
      "It takes courage to acknowledge stress. I'm here to support you. Have you noticed any patterns in when you feel most stressed?"
    ]
  },
  {
    trigger: ["sad", "depressed", "down", "low", "unhappy", "blue"],
    responses: [
      "I hear that you're going through a difficult time. Your feelings are valid, and it's okay to feel this way. Would you like to talk about what's contributing to these feelings?",
      "Thank you for sharing that with me. Depression can feel isolating, but you've taken a brave step by reaching out. How long have you been feeling this way?",
      "I'm here to listen without judgment. Sometimes talking through our feelings can provide clarity. What does a typical day look like for you right now?"
    ]
  },
  {
    trigger: ["angry", "frustrated", "mad", "irritated", "annoyed"],
    responses: [
      "It sounds like you're experiencing some intense emotions. Anger can be a signal that something important to you feels threatened. Can you help me understand what's triggering these feelings?",
      "Frustration is a natural human emotion. Let's work together to understand what's behind these feelings. Have you noticed what tends to set off your anger?",
      "I can sense your frustration. Sometimes anger masks other emotions like hurt or disappointment. Would you like to explore what might be underneath these feelings?"
    ]
  },
  {
    trigger: ["help", "support", "advice", "guidance", "what should i do"],
    responses: [
      "I'm glad you're seeking support - that shows real strength. Could you share more about your specific situation so I can better understand how to help?",
      "Asking for help is a sign of wisdom, not weakness. I'm here to support you through whatever you're facing. What area of your life would you like to focus on?",
      "You've come to the right place for support. Every person's journey is unique. Could you tell me more about what's bringing you here today?"
    ]
  },
  {
    trigger: ["tired", "exhausted", "fatigue", "drained", "worn out"],
    responses: [
      "Physical and emotional exhaustion can be really challenging. Are you getting enough rest, or is this more of an emotional tiredness?",
      "Feeling drained can affect every aspect of our lives. Have you noticed if this tiredness is more physical, mental, or emotional?",
      "Exhaustion often signals that we need to pay attention to our self-care. What does your sleep and daily routine look like?"
    ]
  },
  {
    trigger: ["lonely", "alone", "isolated", "disconnected"],
    responses: [
      "Loneliness can be one of the most painful human experiences. Even in a crowd, we can feel alone. Can you tell me more about these feelings of isolation?",
      "Thank you for sharing something so personal. Feeling disconnected is more common than you might think. Are there people in your life you'd like to feel closer to?",
      "I want you to know that right here, right now, you're not alone. I'm listening. What does loneliness feel like for you?"
    ]
  },
  {
    trigger: ["work", "job", "career", "workplace", "boss", "colleague"],
    responses: [
      "Work-related stress is very common and can significantly impact our mental health. What aspects of your work situation are bothering you most?",
      "Workplace challenges can spill over into all areas of our lives. Are you facing specific issues with tasks, relationships, or work environment?",
      "I understand work can be a major source of stress. Would you like to talk about strategies for managing workplace challenges or setting boundaries?"
    ]
  },
  {
    trigger: ["family", "parents", "relationship", "partner", "spouse", "marriage"],
    responses: [
      "Relationships can be both our greatest source of joy and our biggest challenge. What's happening in your relationships that's concerning you?",
      "Family and relationship dynamics can be complex. It's natural to have ups and downs. Can you share what's been on your mind about your relationships?",
      "Thank you for opening up about your relationships. Communication and boundaries are often key areas to explore. What feels most challenging right now?"
    ]
  },
  {
    trigger: ["sleep", "insomnia", "can't sleep", "nightmares", "dreams"],
    responses: [
      "Sleep issues can really impact our mental health and daily functioning. How long have you been experiencing sleep difficulties?",
      "Quality sleep is crucial for mental wellness. Are you having trouble falling asleep, staying asleep, or both?",
      "Sleep and mental health are closely connected. Have you noticed any patterns in your sleep issues or things that seem to trigger them?"
    ]
  }
];

export const getRandomResponse = (trigger) => {
  const matchedCategory = mockChatResponses.find(category =>
    category.trigger.some(word => 
      trigger.toLowerCase().includes(word.toLowerCase())
    )
  );
  
  if (matchedCategory) {
    const randomIndex = Math.floor(Math.random() * matchedCategory.responses.length);
    return matchedCategory.responses[randomIndex];
  }
  
  // Default responses for unmatched inputs
  const defaultResponses = [
    "I hear you. Can you tell me more about what you're experiencing?",
    "Thank you for sharing that with me. How does that make you feel?",
    "That sounds important to you. Would you like to explore that further?",
    "I'm listening. What thoughts or feelings come up for you around this?",
    "Help me understand better - can you share more about your experience?",
    "That's a lot to process. How are you coping with all of this?",
    "I appreciate you opening up. What support do you feel you need right now?"
  ];
  
  const randomIndex = Math.floor(Math.random() * defaultResponses.length);
  return defaultResponses[randomIndex];
};