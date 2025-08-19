import React from 'react';
import { MessageCircle, Brain, Target, Shield, Clock, Users } from 'lucide-react';

const FeaturesSection = () => {
  const features = [
    {
      icon: MessageCircle,
      title: "Empathetic Conversations",
      description: "Engage in natural, understanding conversations with our AI that listens without judgment and responds with compassion."
    },
    {
      icon: Brain,
      title: "Smart Insights",
      description: "Receive personalized insights based on your conversations, helping you understand patterns and triggers in your mental health."
    },
    {
      icon: Target,
      title: "Personalized Recommendations",
      description: "Get tailored resources including meditation guides, therapy articles, and wellness content based on your current needs."
    },
    {
      icon: Shield,
      title: "Safe & Private",
      description: "Your conversations are secure and confidential. We prioritize your privacy and create a safe space for open dialogue."
    },
    {
      icon: Clock,
      title: "24/7 Availability",
      description: "Access support whenever you need it. Our AI companion is available around the clock to provide assistance and guidance."
    },
    {
      icon: Users,
      title: "Evidence-Based Support",
      description: "Grounded in mental health research and best practices, providing reliable support for your wellness journey."
    }
  ];

  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl lg:text-5xl font-bold text-black mb-6">
            Features That 
            <span className="block bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
              Support Your Journey
            </span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Combining the power of AI with evidence-based mental health support to provide you with comprehensive care.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div 
              key={index}
              className="group p-8 rounded-2xl bg-gray-50 hover:bg-white hover:shadow-xl transition-all duration-300 border border-gray-100 hover:border-gray-200"
            >
              <div className="mb-6">
                <div className="w-16 h-16 bg-black rounded-2xl flex items-center justify-center group-hover:bg-gray-800 transition-colors duration-300">
                  <feature.icon className="text-white" size={28} />
                </div>
              </div>
              <h3 className="text-xl font-semibold text-black mb-4 group-hover:text-gray-800 transition-colors">
                {feature.title}
              </h3>
              <p className="text-gray-600 leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;