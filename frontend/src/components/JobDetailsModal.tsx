import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  X,
  MapPin,
  DollarSign,
  Clock,
  Users,
  Building,
  Send,
  Eye,
  CheckCircle,
  ExternalLink,
} from "lucide-react";
import { showToast } from "./Toast";

interface Job {
  id: string;
  title: string;
  company: string;
  logo: string;
  location: string;
  description: string;
  matchScore: number;
  applied: boolean;
  salary?: string;
  type: "Full-time" | "Part-time" | "Contract";
}

interface JobDetailsModalProps {
  job: Job | null;
  isOpen: boolean;
  onClose: () => void;
  onApply?: (jobId: string) => void;
}

const JobDetailsModal: React.FC<JobDetailsModalProps> = ({
  job,
  isOpen,
  onClose,
  onApply,
}) => {
  const [isApplying, setIsApplying] = useState(false);
  const [showCoverLetter, setShowCoverLetter] = useState(false);

  if (!job) return null;

  const handleApply = async () => {
    setIsApplying(true);

    // Simulate application process
    await new Promise((resolve) => setTimeout(resolve, 2000));

    if (onApply) {
      onApply(job.id);
    }
    setIsApplying(false);
    showToast.success(`Application submitted to ${job.company}!`);
    onClose();
  };

  const coverLetterContent = `Dear ${job.company} Hiring Team,

I am excited to apply for the ${job.title} position at ${job.company}. With my extensive experience in frontend development and proven track record in building scalable web applications, I believe I would be a valuable addition to your team.

My background includes:
• 5+ years of React and TypeScript development
• Experience with modern JavaScript frameworks and tools
• Strong understanding of UI/UX principles
• Proven ability to work in agile development environments

I am particularly drawn to ${job.company} because of your innovative approach to technology and commitment to creating exceptional user experiences. The ${job.title} role aligns perfectly with my career goals and technical expertise.

I would welcome the opportunity to discuss how my skills and enthusiasm can contribute to your team's continued success.

Best regards,
Alex Johnson`;

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-50"
            onClick={onClose}
          />

          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            className="relative bg-white dark:bg-gray-800 rounded-xl shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden"
          >
            <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-teal-500 rounded-lg flex items-center justify-center text-white text-xl font-bold">
                  {job.logo}
                </div>
                <div>
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                    {job.title}
                  </h2>
                  <p className="text-blue-600 dark:text-blue-400 font-medium">
                    {job.company}
                  </p>
                </div>
              </div>
              <button
                onClick={onClose}
                className="p-2 text-gray-400 hover:text-gray-500 dark:hover:text-gray-300"
              >
                <X className="h-6 w-6" />
              </button>
            </div>

            <div className="overflow-y-auto max-h-[calc(90vh-140px)]">
              <div className="p-6">
                <div className="grid md:grid-cols-3 gap-6 mb-6">
                  <div className="flex items-center space-x-2">
                    <MapPin className="h-5 w-5 text-gray-400" />
                    <span className="text-gray-600 dark:text-gray-300">
                      {job.location}
                    </span>
                  </div>
                  {job.salary && (
                    <div className="flex items-center space-x-2">
                      <DollarSign className="h-5 w-5 text-gray-400" />
                      <span className="text-gray-600 dark:text-gray-300">
                        {job.salary}
                      </span>
                    </div>
                  )}
                  <div className="flex items-center space-x-2">
                    <Clock className="h-5 w-5 text-gray-400" />
                    <span className="text-gray-600 dark:text-gray-300">
                      {job.type}
                    </span>
                  </div>
                </div>

                <div className="mb-6">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                      Match Score
                    </h3>
                    <span className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                      {job.matchScore}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div
                      className="bg-gradient-to-r from-blue-500 to-teal-500 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${job.matchScore}%` }}
                    />
                  </div>
                </div>

                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                    Job Description
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                    {job.description}
                  </p>

                  <div className="mt-4 space-y-4">
                    <div>
                      <h4 className="font-medium text-gray-900 dark:text-white mb-2">
                        What you'll do:
                      </h4>
                      <ul className="space-y-1 text-gray-600 dark:text-gray-300">
                        <li>
                          • Build responsive web applications using modern
                          frameworks
                        </li>
                        <li>
                          • Collaborate with designers and backend developers
                        </li>
                        <li>
                          • Optimize applications for performance and
                          scalability
                        </li>
                        <li>
                          • Participate in code reviews and technical
                          discussions
                        </li>
                      </ul>
                    </div>

                    <div>
                      <h4 className="font-medium text-gray-900 dark:text-white mb-2">
                        Requirements:
                      </h4>
                      <ul className="space-y-1 text-gray-600 dark:text-gray-300">
                        <li>• 3+ years of React/TypeScript experience</li>
                        <li>
                          • Strong understanding of modern web technologies
                        </li>
                        <li>• Experience with version control systems (Git)</li>
                        <li>
                          • Excellent problem-solving and communication skills
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>

                {showCoverLetter && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    exit={{ opacity: 0, height: 0 }}
                    className="mb-6"
                  >
                    <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
                      <div className="flex items-center justify-between mb-3">
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                          AI-Generated Cover Letter
                        </h3>
                        <div className="flex space-x-2">
                          <button className="px-3 py-1 text-sm bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 rounded-md hover:bg-green-200 dark:hover:bg-green-900/50">
                            Approve
                          </button>
                          <button className="px-3 py-1 text-sm bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded-md hover:bg-blue-200 dark:hover:bg-blue-900/50">
                            Edit
                          </button>
                          <button className="px-3 py-1 text-sm bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 rounded-md hover:bg-red-200 dark:hover:bg-red-900/50">
                            Reject
                          </button>
                        </div>
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-300 whitespace-pre-line font-mono">
                        {coverLetterContent}
                      </div>
                    </div>
                  </motion.div>
                )}
              </div>
            </div>

            <div className="p-6 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
              <div className="flex items-center justify-between">
                <div className="flex space-x-3">
                  <button
                    onClick={() => setShowCoverLetter(!showCoverLetter)}
                    className="inline-flex items-center px-4 py-2 text-gray-600 dark:text-gray-300 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                  >
                    <Eye className="h-4 w-4 mr-2" />
                    {showCoverLetter ? "Hide" : "Preview"} Cover Letter
                  </button>

                  <button className="inline-flex items-center px-4 py-2 text-gray-600 dark:text-gray-300 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
                    <ExternalLink className="h-4 w-4 mr-2" />
                    View on Company Site
                  </button>
                </div>

                {job.applied ? (
                  <div className="inline-flex items-center text-green-600 dark:text-green-400 font-medium">
                    <CheckCircle className="h-5 w-5 mr-2" />
                    Application Submitted
                  </div>
                ) : (
                  <button
                    onClick={handleApply}
                    disabled={isApplying}
                    className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-blue-600 to-teal-600 text-white font-medium rounded-lg hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-300 disabled:opacity-50 disabled:transform-none"
                  >
                    {isApplying ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>
                        Submitting Application...
                      </>
                    ) : (
                      <>
                        <Send className="h-4 w-4 mr-2" />
                        Apply Now
                      </>
                    )}
                  </button>
                )}
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};

export default JobDetailsModal;
