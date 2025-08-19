import React from 'react';
import { Mail, Github, Linkedin, Phone, AlertTriangle } from 'lucide-react';

const ContactSection = () => {
  return (
    <section id="contact" className="py-20 bg-white">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl lg:text-5xl font-bold text-black mb-6">
            Get In 
            <span className="bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
              {" "}Touch
            </span>
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
            Have questions about psychMASTER? Want to learn more about our technology or provide feedback? 
            We'd love to hear from you.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-12">
          <div className="space-y-8">
            <div>
              <h3 className="text-2xl font-semibold text-black mb-6">Contact Information</h3>
              <div className="space-y-4">
                <div className="flex items-center space-x-4">
                  <div className="w-10 h-10 bg-black rounded-lg flex items-center justify-center">
                    <Mail className="text-white" size={20} />
                  </div>
                  <div>
                    <p className="font-semibold text-black">Email</p>
                    <p className="text-gray-600">contact@psychmaster.ai</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-4">
                  <div className="w-10 h-10 bg-black rounded-lg flex items-center justify-center">
                    <Github className="text-white" size={20} />
                  </div>
                  <div>
                    <p className="font-semibold text-black">GitHub</p>
                    <p className="text-gray-600">github.com/psychmaster</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-4">
                  <div className="w-10 h-10 bg-black rounded-lg flex items-center justify-center">
                    <Linkedin className="text-white" size={20} />
                  </div>
                  <div>
                    <p className="font-semibold text-black">LinkedIn</p>
                    <p className="text-gray-600">linkedin.com/company/psychmaster</p>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-2xl font-semibold text-black mb-6">Academic & Research</h3>
              <p className="text-gray-600 leading-relaxed mb-4">
                This project represents innovative research in AI-powered mental health support, 
                combining traditional machine learning with modern LLM technology for real-world applications.
              </p>
              <p className="text-gray-600 leading-relaxed">
                For research inquiries, collaboration opportunities, or technical discussions, 
                please reach out through the contact information provided.
              </p>
            </div>
          </div>

          <div className="bg-gray-50 rounded-2xl p-8">
            <div className="flex items-start space-x-4 mb-6">
              <div className="w-10 h-10 bg-red-600 rounded-lg flex items-center justify-center flex-shrink-0">
                <AlertTriangle className="text-white" size={20} />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-black mb-2">Important Disclaimer</h3>
                <p className="text-gray-600 text-sm leading-relaxed">
                  psychMASTER is an AI tool designed for awareness and support purposes only. 
                  It is not intended to replace professional medical advice, diagnosis, or treatment.
                </p>
              </div>
            </div>

            <div className="space-y-4">
              <div className="bg-white rounded-lg p-4 border border-gray-200">
                <h4 className="font-semibold text-black mb-2">Crisis Resources</h4>
                <div className="space-y-2 text-sm">
                  <p className="text-gray-600">
                    <strong>National Suicide Prevention Lifeline:</strong><br />
                    <a href="tel:988" className="text-black hover:underline">988 (US)</a>
                  </p>
                  <p className="text-gray-600">
                    <strong>Crisis Text Line:</strong><br />
                    Text HOME to <a href="sms:741741" className="text-black hover:underline">741741</a>
                  </p>
                  <p className="text-gray-600">
                    <strong>International Association for Suicide Prevention:</strong><br />
                    <a href="https://www.iasp.info/resources/Crisis_Centres/" target="_blank" rel="noopener noreferrer" className="text-black hover:underline">
                      Find local crisis centers
                    </a>
                  </p>
                </div>
              </div>

              <div className="bg-white rounded-lg p-4 border border-gray-200">
                <h4 className="font-semibold text-black mb-2">Professional Help</h4>
                <p className="text-gray-600 text-sm leading-relaxed">
                  If you're experiencing persistent mental health concerns, please consult with 
                  a qualified healthcare professional, therapist, or counselor in your area.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ContactSection;