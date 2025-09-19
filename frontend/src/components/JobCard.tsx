import React, { useState } from "react";
import { motion } from "framer-motion";
import {
  MapPin,
  DollarSign,
  Clock,
  ExternalLink,
  Eye,
  Send,
  CheckCircle,
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

interface JobCardProps {
  job: Job;
  onViewDetails: (job: Job) => void;
  onApply?: (jobId: string) => void;
}

const JobCard: React.FC<JobCardProps> = ({ job, onViewDetails, onApply }) => {
  const [isApplying, setIsApplying] = useState(false);

  const handleApply = async (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsApplying(true);

    // Simulate application process
    await new Promise((resolve) => setTimeout(resolve, 1500));

    if (onApply) {
      onApply(job.id);
    }
    setIsApplying(false);
    showToast.success(`Application submitted to ${job.company}!`);
  };

  const getMatchScoreColor = (score: number) => {
    if (score >= 90)
      return "text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900/30";
    if (score >= 75)
      return "text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-900/30";
    if (score >= 60)
      return "text-yellow-600 dark:text-yellow-400 bg-yellow-100 dark:bg-yellow-900/30";
    return "text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-900/30";
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -4 }}
      transition={{ duration: 0.3 }}
      className="bg-white dark:bg-gray-800 rounded-xl shadow-sm hover:shadow-lg border border-gray-200 dark:border-gray-700 p-6 cursor-pointer"
      onClick={() => onViewDetails(job)}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-start space-x-4">
          <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-teal-500 rounded-lg flex items-center justify-center text-white text-xl font-bold">
            {job.logo}
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white truncate">
              {job.title}
            </h3>
            <p className="text-blue-600 dark:text-blue-400 font-medium">
              {job.company}
            </p>
          </div>
        </div>

        <div
          className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getMatchScoreColor(
            job.matchScore
          )}`}
        >
          {job.matchScore}% match
        </div>
      </div>

      <p className="text-gray-600 dark:text-gray-300 text-sm mb-4 line-clamp-2">
        {job.description}
      </p>

      <div className="flex items-center space-x-4 mb-4 text-sm text-gray-500 dark:text-gray-400">
        <div className="flex items-center space-x-1">
          <MapPin className="h-4 w-4" />
          <span>{job.location}</span>
        </div>
        {job.salary && (
          <div className="flex items-center space-x-1">
            <DollarSign className="h-4 w-4" />
            <span>{job.salary}</span>
          </div>
        )}
        <div className="flex items-center space-x-1">
          <Clock className="h-4 w-4" />
          <span>{job.type}</span>
        </div>
      </div>

      <div className="flex items-center justify-between">
        <button
          onClick={(e) => {
            e.stopPropagation();
            onViewDetails(job);
          }}
          className="inline-flex items-center text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 text-sm font-medium"
        >
          <Eye className="h-4 w-4 mr-1" />
          View Details
        </button>

        {job.applied ? (
          <div className="inline-flex items-center text-green-600 dark:text-green-400 text-sm font-medium">
            <CheckCircle className="h-4 w-4 mr-1" />
            Applied
          </div>
        ) : (
          <button
            onClick={handleApply}
            disabled={isApplying}
            className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-blue-600 to-teal-600 text-white text-sm font-medium rounded-lg hover:shadow-lg transition-all duration-300 disabled:opacity-50"
          >
            {isApplying ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>
                Applying...
              </>
            ) : (
              <>
                <Send className="h-4 w-4 mr-2" />
                Quick Apply
              </>
            )}
          </button>
        )}
      </div>
    </motion.div>
  );
};

export default JobCard;
