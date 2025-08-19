import React from 'react';
import { ArrowRight, Heart, Brain, MessageSquare } from 'lucide-react';

const HeroSection = () => {
  const scrollToChat = () => {
    const element = document.getElementById('chat');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section id="hero" className="pt-16 min-h-screen flex items-center bg-gradient-to-br from-gray-50 to-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-8">
            <div className="space-y-4">
              <h1 className="text-5xl lg:text-7xl font-bold text-black leading-tight">
                Your AI Companion for 
                <span className="block bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                  Mental Health
                </span>
              </h1>
              <p className="text-xl text-gray-600 leading-relaxed max-w-2xl">
                Experience empathetic conversations powered by advanced AI technology. 
                Get personalized insights and recommendations tailored to your mental wellness journey.
              </p>
            </div>
            
            <div className="flex flex-col sm:flex-row gap-4">
              <button 
                onClick={scrollToChat}
                className="bg-black text-white px-8 py-4 rounded-lg font-semibold hover:bg-gray-800 transition-all duration-300 flex items-center justify-center group"
              >
                Start Chatting
                <ArrowRight className="ml-2 group-hover:translate-x-1 transition-transform" size={20} />
              </button>
              <button 
                onClick={() => document.getElementById('about').scrollIntoView({ behavior: 'smooth' })}
                className="border-2 border-black text-black px-8 py-4 rounded-lg font-semibold hover:bg-black hover:text-white transition-all duration-300"
              >
                Learn More
              </button>
            </div>

            <div className="flex items-center space-x-8 pt-8">
              <div className="flex items-center space-x-2">
                <Heart className="text-gray-800" size={24} />
                <span className="text-sm text-gray-600">Empathetic AI</span>
              </div>
              <div className="flex items-center space-x-2">
                <Brain className="text-gray-800" size={24} />
                <span className="text-sm text-gray-600">Smart Insights</span>
              </div>
              <div className="flex items-center space-x-2">
                <MessageSquare className="text-gray-800" size={24} />
                <span className="text-sm text-gray-600">24/7 Available</span>
              </div>
            </div>
          </div>
          
          <div className="relative">
            <div className="bg-gray-900 rounded-2xl p-8 shadow-2xl transform rotate-3 hover:rotate-0 transition-transform duration-500">
              <div className="bg-white rounded-xl p-6 space-y-4">
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-gray-900 rounded-full flex items-center justify-center">
                    <MessageSquare className="text-white" size={16} />
                  </div>
                  <div className="flex-1">
                    <p className="text-sm text-gray-600 mb-2">psychMASTER</p>
                    <p className="text-gray-900">Hello! I'm here to listen and support you. How are you feeling today?</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-gray-200 rounded-full"></div>
                  <div className="flex-1">
                    <p className="text-sm text-gray-600 mb-2">You</p>
                    <p className="text-gray-900">I've been feeling a bit overwhelmed lately with work and life...</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-gray-900 rounded-full flex items-center justify-center">
                    <MessageSquare className="text-white" size={16} />
                  </div>
                  <div className="flex-1">
                    <p className="text-sm text-gray-600 mb-2">psychMASTER</p>
                    <p className="text-gray-900">I understand that feeling. Let's explore some strategies that might help...</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;