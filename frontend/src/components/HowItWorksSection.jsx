import React from 'react';
import { MessageSquare, Search, Lightbulb } from 'lucide-react';

const HowItWorksSection = () => {
  const steps = [
    {
      step: "01",
      icon: MessageSquare,
      title: "Start Chatting",
      description: "Begin a conversation with our AI companion. Share your thoughts, feelings, and experiences in a safe, judgment-free environment."
    },
    {
      step: "02", 
      icon: Search,
      title: "AI Analysis",
      description: "Our advanced AI analyzes your conversation patterns and emotional cues to better understand your mental health state and needs."
    },
    {
      step: "03",
      icon: Lightbulb,
      title: "Get Personalized Support",
      description: "Receive tailored recommendations including coping strategies, resources, and guidance based on your unique situation and needs."
    }
  ];

  return (
    <section className="py-20 bg-gradient-to-br from-gray-50 to-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl lg:text-5xl font-bold text-black mb-6">
            How 
            <span className="bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
              {" "}It Works
            </span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Our simple three-step process combines empathetic AI conversation with intelligent analysis to provide personalized mental health support.
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8 lg:gap-12">
          {steps.map((step, index) => (
            <div key={index} className="relative group">
              {/* Connection line for desktop */}
              {index < steps.length - 1 && (
                <div className="hidden lg:block absolute top-20 left-full w-full h-0.5 bg-gray-200 transform -translate-x-1/2 z-0">
                  <div className="absolute right-0 top-1/2 transform -translate-y-1/2 w-3 h-3 bg-gray-400 rounded-full"></div>
                </div>
              )}
              
              <div className="relative z-10 text-center">
                <div className="mb-8">
                  <div className="relative inline-block">
                    <div className="w-20 h-20 bg-black rounded-2xl flex items-center justify-center group-hover:bg-gray-800 transition-colors duration-300 mx-auto">
                      <step.icon className="text-white" size={32} />
                    </div>
                    <div className="absolute -top-2 -right-2 w-8 h-8 bg-white border-2 border-gray-200 rounded-full flex items-center justify-center">
                      <span className="text-xs font-bold text-gray-900">{step.step}</span>
                    </div>
                  </div>
                </div>
                
                <h3 className="text-2xl font-semibold text-black mb-4">
                  {step.title}
                </h3>
                
                <p className="text-gray-600 leading-relaxed max-w-sm mx-auto">
                  {step.description}
                </p>
              </div>
            </div>
          ))}
        </div>
        
        <div className="text-center mt-16">
          <button 
            onClick={() => document.getElementById('chat').scrollIntoView({ behavior: 'smooth' })}
            className="bg-black text-white px-8 py-4 rounded-lg font-semibold hover:bg-gray-800 transition-all duration-300 group"
          >
            Try It Now
            <span className="ml-2 group-hover:translate-x-1 transition-transform inline-block">→</span>
          </button>
        </div>
      </div>
    </section>
  );
};

export default HowItWorksSection;