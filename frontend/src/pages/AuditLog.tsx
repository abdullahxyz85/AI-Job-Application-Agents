import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  FileText,
  Search,
  PenTool,
  Shield,
  Clock,
  CheckCircle,
  AlertCircle,
  XCircle,
} from "lucide-react";
import { useAuth } from "../contexts/AuthContext";

interface AuditLogEntry {
  id: string;
  agent: string;
  action: string;
  details: string;
  status: "success" | "pending" | "error";
  timestamp: Date;
}

const AuditLog: React.FC = () => {
  const { user } = useAuth();
  const [auditLog, setAuditLog] = useState<AuditLogEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Simulate audit log data for now - this would come from backend in production
  useEffect(() => {
    if (user) {
      // Create sample audit log entries based on user data
      const sampleEntries: AuditLogEntry[] = [
        {
          id: "1",
          agent: "resume-parser",
          action: "Resume Analyzed",
          details: `Successfully parsed resume and extracted ${user.skills.length} skills`,
          status: "success",
          timestamp: new Date(Date.now() - 1000 * 60 * 15), // 15 minutes ago
        },
        {
          id: "2",
          agent: "job-searcher",
          action: "Job Search Completed",
          details: "Found 25 matching job opportunities based on your profile",
          status: "success",
          timestamp: new Date(Date.now() - 1000 * 60 * 10), // 10 minutes ago
        },
      ];

      // Add profile creation entry
      if (user.created_at) {
        sampleEntries.unshift({
          id: "0",
          agent: "system",
          action: "Profile Created",
          details: `Welcome! Your AI job application profile has been successfully created`,
          status: "success",
          timestamp: new Date(user.created_at),
        });
      }

      // Add resume upload entry if resume is uploaded
      if (user.resume_uploaded) {
        sampleEntries.push({
          id: "3",
          agent: "resume-parser",
          action: "Resume Uploaded",
          details: "PDF resume successfully uploaded and queued for processing",
          status: "success",
          timestamp: new Date(Date.now() - 1000 * 60 * 5), // 5 minutes ago
        });
      }

      // Sort by timestamp descending (newest first)
      sampleEntries.sort(
        (a, b) => b.timestamp.getTime() - a.timestamp.getTime()
      );

      setAuditLog(sampleEntries);
    }
    setIsLoading(false);
  }, [user]);

  const getAgentIcon = (agent: string) => {
    switch (agent) {
      case "resume-parser":
        return FileText;
      case "job-searcher":
        return Search;
      case "cover-letter-generator":
        return PenTool;
      case "auditor":
        return Shield;
      case "system":
        return Shield;
      default:
        return Clock;
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "success":
        return CheckCircle;
      case "pending":
        return AlertCircle;
      case "error":
        return XCircle;
      default:
        return Clock;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "success":
        return "text-green-600 dark:text-green-400 bg-green-50 dark:bg-green-900/20";
      case "pending":
        return "text-yellow-600 dark:text-yellow-400 bg-yellow-50 dark:bg-yellow-900/20";
      case "error":
        return "text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20";
      default:
        return "text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-900/20";
    }
  };

  const getAgentColor = (agent: string) => {
    switch (agent) {
      case "resume-parser":
        return "from-blue-500 to-blue-600";
      case "job-searcher":
        return "from-teal-500 to-teal-600";
      case "cover-letter-generator":
        return "from-purple-500 to-purple-600";
      case "auditor":
        return "from-orange-500 to-orange-600";
      case "system":
        return "from-gray-500 to-gray-600";
      default:
        return "from-gray-500 to-gray-600";
    }
  };

  const formatTime = (date: Date) => {
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / 60000);

    if (minutes < 1) return "Just now";
    if (minutes < 60) return `${minutes}m ago`;
    if (minutes < 1440) return `${Math.floor(minutes / 60)}h ago`;
    return date.toLocaleDateString();
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading audit log...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Audit Log
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Track all AI agent activities and application progress
          </p>
        </motion.div>

        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
              Agent Activity Timeline
            </h2>
            <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
              Real-time updates from your AI job application agents
            </p>
          </div>

          <div className="p-6">
            <div className="space-y-6">
              {auditLog.map((entry, index) => {
                const AgentIcon = getAgentIcon(entry.agent);
                const StatusIcon = getStatusIcon(entry.status);

                return (
                  <motion.div
                    key={entry.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="relative flex items-start space-x-4"
                  >
                    {/* Timeline line */}
                    {index < auditLog.length - 1 && (
                      <div className="absolute left-6 top-12 w-0.5 h-8 bg-gray-200 dark:bg-gray-700"></div>
                    )}

                    {/* Agent icon */}
                    <div
                      className={`flex-shrink-0 w-12 h-12 rounded-lg bg-gradient-to-r ${getAgentColor(
                        entry.agent
                      )} flex items-center justify-center`}
                    >
                      <AgentIcon className="h-6 w-6 text-white" />
                    </div>

                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4">
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center space-x-2">
                            <h3 className="text-sm font-semibold text-gray-900 dark:text-white">
                              {entry.action}
                            </h3>
                            <div
                              className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(
                                entry.status
                              )}`}
                            >
                              <StatusIcon className="h-3 w-3 mr-1" />
                              {entry.status}
                            </div>
                          </div>
                          <span className="text-xs text-gray-500 dark:text-gray-400">
                            {formatTime(entry.timestamp)}
                          </span>
                        </div>

                        <p className="text-sm text-gray-600 dark:text-gray-300 mb-2">
                          {entry.details}
                        </p>

                        <div className="flex items-center space-x-2 text-xs text-gray-500 dark:text-gray-400">
                          <span className="capitalize">
                            {entry.agent.replace("-", " ")} Agent
                          </span>
                          <span>•</span>
                          <span>{entry.timestamp.toLocaleTimeString()}</span>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                );
              })}
            </div>

            {auditLog.length === 0 && (
              <div className="text-center py-12">
                <Clock className="h-16 w-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  No Activity Yet
                </h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Upload your resume to start seeing agent activity
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Summary Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mt-8"
        >
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Total Actions
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {auditLog.length}
                  </p>
                </div>
                <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                  <Clock className="h-6 w-6 text-white" />
                </div>
              </div>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Successful Actions
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {
                      auditLog.filter((entry) => entry.status === "success")
                        .length
                    }
                  </p>
                </div>
                <div className="w-12 h-12 bg-gradient-to-r from-green-500 to-green-600 rounded-lg flex items-center justify-center">
                  <CheckCircle className="h-6 w-6 text-white" />
                </div>
              </div>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Active Agents
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    4
                  </p>
                </div>
                <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <Shield className="h-6 w-6 text-white" />
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default AuditLog;
