import React from 'react';
import { Link } from 'react-router-dom';
import { FileText, Users, Brain, Zap, Shield, Globe } from 'lucide-react';

const Home = () => {
  const features = [
    {
      icon: FileText,
      title: 'PDF Outline Extraction',
      description: 'Automatically extract hierarchical outlines from PDF documents with intelligent heading detection.',
      color: 'bg-blue-500',
    },
    {
      icon: Users,
      title: 'Persona-Driven Analysis',
      description: 'Get personalized insights based on your role, goals, and specific job-to-be-done scenarios.',
      color: 'bg-green-500',
    },
    {
      icon: Brain,
      title: 'Intelligent Recommendations',
      description: 'AI-powered section ranking and relevance scoring to surface the most important content.',
      color: 'bg-purple-500',
    },
    {
      icon: Zap,
      title: 'Fast Processing',
      description: 'Lightweight models ensure quick processing times while maintaining high accuracy.',
      color: 'bg-yellow-500',
    },
    {
      icon: Shield,
      title: 'Offline Processing',
      description: 'All processing happens locally with no data sent to external servers.',
      color: 'bg-red-500',
    },
    {
      icon: Globe,
      title: 'Interactive Viewer',
      description: 'Seamless integration with Adobe PDF Embed API for enhanced document viewing.',
      color: 'bg-indigo-500',
    },
  ];

  const quickActions = [
    {
      title: 'Upload & Analyze PDF',
      description: 'Extract outline from a single PDF document',
      path: '/viewer',
      color: 'from-blue-500 to-blue-600',
    },
    {
      title: 'Persona Analysis',
      description: 'Analyze multiple PDFs with persona-driven insights',
      path: '/persona-analysis',
      color: 'from-green-500 to-green-600',
    },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Hero Section */}
      <div className="text-center mb-16">
        <h1 className="text-4xl font-bold text-gray-900 mb-6">
          Intelligent PDF Research Companion
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          Transform static PDF libraries into dynamic, persona-driven knowledge systems. 
          Extract structure, surface insights, and personalize document views based on your specific needs.
        </p>
        <div className="flex justify-center space-x-4">
          <Link
            to="/viewer"
            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors"
          >
            Get Started
          </Link>
          <Link
            to="/persona-analysis"
            className="bg-gray-100 text-gray-700 px-6 py-3 rounded-lg font-medium hover:bg-gray-200 transition-colors"
          >
            Learn More
          </Link>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mb-16">
        <h2 className="text-2xl font-bold text-gray-900 mb-8 text-center">
          Quick Actions
        </h2>
        <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
          {quickActions.map((action, index) => (
            <Link
              key={index}
              to={action.path}
              className={`bg-gradient-to-r ${action.color} text-white p-6 rounded-lg hover:shadow-lg transition-all transform hover:-translate-y-1`}
            >
              <h3 className="text-xl font-semibold mb-2">{action.title}</h3>
              <p className="text-blue-100">{action.description}</p>
            </Link>
          ))}
        </div>
      </div>

      {/* Features Grid */}
      <div className="mb-16">
        <h2 className="text-2xl font-bold text-gray-900 mb-8 text-center">
          Key Features
        </h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div
                key={index}
                className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow"
              >
                <div className={`${feature.color} w-12 h-12 rounded-lg flex items-center justify-center mb-4`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Technical Specifications */}
      <div className="bg-gray-50 rounded-lg p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
          Technical Specifications
        </h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600 mb-2">≤200MB</div>
            <div className="text-gray-600">Round 1A Model Size</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600 mb-2">≤1GB</div>
            <div className="text-gray-600">Round 1B Model Size</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-purple-600 mb-2">≤10s</div>
            <div className="text-gray-600">Round 1A Runtime</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-yellow-600 mb-2">≤60s</div>
            <div className="text-gray-600">Round 1B Runtime</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home; 