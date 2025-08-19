import React from 'react';
import { Brain, Zap, Target, Shield } from 'lucide-react';

const AboutSection = () => {
  const highlights = [
    {
      icon: Brain,
      title: "Advanced AI Technology",
      description: "Powered by state-of-the-art language models and machine learning algorithms designed for empathetic conversation."
    },
    {
      icon: Zap,
      title: "Real-Time Analysis",
      description: "Continuous analysis of conversation patterns to provide immediate, contextually relevant support and recommendations."
    },
    {
      icon: Target,
      title: "Personalized Approach",
      description: "Tailored responses and resources based on individual needs, mental health patterns, and conversation history."
    },
    {
      icon: Shield,
      title: "Privacy & Safety First",
      description: "Built with privacy by design principles, ensuring your conversations remain confidential and secure."
    }
  ];

  return (
    <section id="about" className="py-20 bg-gradient-to-br from-gray-50 to-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          <div className="space-y-8">
            <div>
              <h2 className="text-4xl lg:text-5xl font-bold text-black mb-6 leading-tight">
                Why This 
                <span className="block bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                  Matters
                </span>
              </h2>
              <div className="space-y-6 text-gray-600 leading-relaxed">
                <p className="text-lg">
                  Mental health challenges affect millions of people worldwide, yet access to support 
                  remains limited by availability, cost, and stigma. psychMASTER bridges this gap by 
                  providing immediate, accessible, and judgment-free mental health support.
                </p>
                <p>
                  Our platform combines the conversational abilities of Large Language Models (LLMs) 
                  with structured decision-making of machine learning classification models. This hybrid 
                  approach enables us to provide both empathetic conversation and data-driven insights.
                </p>
                <p>
                  While chatting, our system continuously analyzes inputs using trained classification 
                  models to predict mental health categories and provide personalized resources such as 
                  meditation guides, therapy blogs, emergency helplines, or motivational content.
                </p>
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <h3 className="text-2xl font-semibold text-black mb-8">Our Approach</h3>
            {highlights.map((highlight, index) => (
              <div key={index} className="flex space-x-4 group">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 bg-black rounded-xl flex items-center justify-center group-hover:bg-gray-800 transition-colors">
                    <highlight.icon className="text-white" size={20} />
                  </div>
                </div>
                <div>
                  <h4 className="text-lg font-semibold text-black mb-2">{highlight.title}</h4>
                  <p className="text-gray-600 leading-relaxed">{highlight.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-20 bg-white rounded-2xl p-8 lg:p-12 shadow-xl border border-gray-200">
          <div className="text-center mb-12">
            <h3 className="text-3xl font-bold text-black mb-4">Project Contributions</h3>
            <p className="text-gray-600 max-w-3xl mx-auto">
              This project demonstrates three key innovations in AI-powered mental health support:
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-gray-900 to-gray-700 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <span className="text-white font-bold text-xl">1</span>
              </div>
              <h4 className="text-xl font-semibold text-black mb-3">Enhanced ML Models</h4>
              <p className="text-gray-600">
                Evolution from baseline classifiers to advanced hybrid methods using sentence embeddings 
                and ensemble models for improved accuracy.
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-gray-900 to-gray-700 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <span className="text-white font-bold text-xl">2</span>
              </div>
              <h4 className="text-xl font-semibold text-black mb-3">Real-Time LLM Integration</h4>
              <p className="text-gray-600">
                Seamless integration of classification models with conversational AI to provide 
                continuous insights during chat interactions.
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-gray-900 to-gray-700 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <span className="text-white font-bold text-xl">3</span>
              </div>
              <h4 className="text-xl font-semibold text-black mb-3">Personalized Recommendations</h4>
              <p className="text-gray-600">
                Dynamic resource suggestions including videos, blogs, and helplines based on 
                predicted user mental health state.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AboutSection;