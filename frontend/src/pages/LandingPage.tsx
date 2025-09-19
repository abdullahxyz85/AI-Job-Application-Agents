import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { useAuth } from "../contexts/AuthContext";
import {
  ArrowRight,
  FileText,
  Search,
  PenTool,
  Shield,
  Zap,
  Users,
  Trophy,
  Bot,
  UserPlus,
  LogIn,
} from "lucide-react";

const LandingPage: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const fadeInUp = {
    initial: { opacity: 0, y: 60 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.6 },
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-teal-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8 }}
              className="mb-8"
            >
              <div className="inline-flex items-center justify-center p-2 bg-gradient-to-r from-blue-600 to-teal-600 rounded-full mb-4">
                <Bot className="h-16 w-16 text-white" />
              </div>
              <h1 className="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
                AI-Powered Job
                <span className="bg-gradient-to-r from-blue-600 to-teal-600 bg-clip-text text-transparent">
                  {" "}
                  Application Agent
                </span>
              </h1>
            </motion.div>

            <motion.p
              {...fadeInUp}
              className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed"
            >
              Stop spending hours on job applications. Our multi-agent AI system
              automatically parses your resume, finds matching opportunities,
              and crafts personalized cover letters.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, duration: 0.6 }}
              className="mb-16"
            >
              {isAuthenticated ? (
                <Link
                  to="/dashboard"
                  className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-teal-600 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300 text-lg"
                >
                  Go to Dashboard
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
              ) : (
                <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
                  <Link
                    to="/signup"
                    className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-teal-600 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300 text-lg"
                  >
                    <UserPlus className="mr-2 h-5 w-5" />
                    Sign Up Free
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Link>
                  <Link
                    to="/signin"
                    className="inline-flex items-center px-8 py-4 bg-white dark:bg-gray-800 text-gray-900 dark:text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300 text-lg border border-gray-200 dark:border-gray-700"
                  >
                    <LogIn className="mr-2 h-5 w-5" />
                    Sign In
                  </Link>
                </div>
              )}
            </motion.div>
          </div>
        </div>
      </div>

      {/* Multi-Agent System Visualization */}
      <div className="py-20 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Four AI Agents Working for You
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Our intelligent agents collaborate to streamline your entire job
              application process
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                icon: FileText,
                name: "Resume Parser",
                description:
                  "Extracts skills, experience, and qualifications from your resume",
                color: "from-blue-500 to-blue-600",
                delay: 0.1,
              },
              {
                icon: Search,
                name: "Job Searcher",
                description:
                  "Finds and ranks opportunities based on your profile match",
                color: "from-teal-500 to-teal-600",
                delay: 0.2,
              },
              {
                icon: PenTool,
                name: "Cover Letter Generator",
                description:
                  "Creates personalized cover letters for each application",
                color: "from-purple-500 to-purple-600",
                delay: 0.3,
              },
              {
                icon: Shield,
                name: "Application Auditor",
                description: "Reviews and tracks all application activities",
                color: "from-orange-500 to-orange-600",
                delay: 0.4,
              },
            ].map((agent) => (
              <motion.div
                key={agent.name}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: agent.delay, duration: 0.6 }}
                className="relative group"
              >
                <div className="bg-white dark:bg-gray-900 rounded-xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-200 dark:border-gray-700 group-hover:border-transparent">
                  <div
                    className={`inline-flex items-center justify-center w-12 h-12 rounded-lg bg-gradient-to-r ${agent.color} mb-4`}
                  >
                    <agent.icon className="h-6 w-6 text-white" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    {agent.name}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300 text-sm">
                    {agent.description}
                  </p>
                  <div
                    className={`absolute inset-0 bg-gradient-to-r ${agent.color} opacity-0 group-hover:opacity-5 rounded-xl transition-opacity duration-300`}
                  ></div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* Benefits Section */}
      <div className="py-20 bg-gray-50 dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Why Choose AI Job Agent?
            </h2>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: Zap,
                title: "Lightning Fast",
                description: "Apply to multiple jobs in minutes, not hours",
              },
              {
                icon: Users,
                title: "Personalized Approach",
                description:
                  "Every application is tailored to the specific role",
              },
              {
                icon: Trophy,
                title: "Higher Success Rate",
                description:
                  "AI-optimized applications get more interview calls",
              },
            ].map((benefit, index) => (
              <motion.div
                key={benefit.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1, duration: 0.6 }}
                className="text-center"
              >
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-r from-blue-500 to-teal-500 mb-6">
                  <benefit.icon className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                  {benefit.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-300">
                  {benefit.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-20">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-6">
              Ready to Transform Your Job Search?
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">
              Join thousands of professionals who have accelerated their career
              with AI
            </p>
            {isAuthenticated ? (
              <Link
                to="/dashboard"
                className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-teal-600 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300 text-lg"
              >
                Go to Dashboard
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            ) : (
              <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
                <Link
                  to="/signup"
                  className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-teal-600 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300 text-lg"
                >
                  <UserPlus className="mr-2 h-5 w-5" />
                  Get Started Now
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
                <Link
                  to="/signin"
                  className="inline-flex items-center px-6 py-3 bg-white dark:bg-gray-800 text-gray-900 dark:text-white font-medium rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300"
                >
                  <LogIn className="mr-2 h-4 w-4" />
                  Sign In
                </Link>
              </div>
            )}
          </motion.div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 dark:bg-gray-950 text-white py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <Bot className="h-6 w-6 text-blue-400" />
            <span className="text-sm text-gray-400">
              Built with Coral Studio Agents
            </span>
          </div>
          <p className="text-gray-400 text-sm">
            Empowering careers through intelligent automation
          </p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
