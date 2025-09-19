import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  Upload,
  Brain,
  Search,
  FileText,
  CheckCircle,
  AlertCircle,
  Clock,
  Zap,
  Download,
  Eye,
} from "lucide-react";
import { showToast } from "../components/Toast";

interface AgentStatus {
  agent_id: string;
  status:
    | "initializing"
    | "parsing_resume"
    | "searching_jobs"
    | "generating_cover_letters"
    | "completed"
    | "error";
  current_step: string;
  progress: number;
  results?: {
    resume: any;
    jobs_found: number;
    matching_jobs: any[];
    cover_letters: any[];
    completion_time: string;
  };
}

interface ResumeData {
  id: string;
  filename: string;
  parsed_data: {
    name: string;
    email: string;
    skills: string[];
    experience_level: string;
    years_experience: string;
    education: string;
    summary: string;
  };
}

const AIJobApplication: React.FC = () => {
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [resumeData, setResumeData] = useState<ResumeData | null>(null);
  const [agentStatus, setAgentStatus] = useState<AgentStatus | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [results, setResults] = useState<any>(null);

  const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (
      !file.name.toLowerCase().endsWith(".pdf") &&
      !file.type.includes("pdf")
    ) {
      showToast.error("Please upload a PDF file");
      return;
    }

    setResumeFile(file);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://localhost:8000/api/resume/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to upload resume");
      }

      const data = await response.json();
      setResumeData(data.resume_data);
      showToast.success("Resume uploaded and parsed successfully!");
    } catch (error) {
      console.error("Upload error:", error);
      showToast.error("Failed to upload resume");
    }
  };

  const startJobApplication = async () => {
    if (!resumeData) {
      showToast.error("Please upload a resume first");
      return;
    }

    setIsProcessing(true);

    try {
      const response = await fetch(
        "http://localhost:8000/api/job-application/start",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            resume_data: resumeData,
            preferences: {},
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to start job application process");
      }

      const data = await response.json();
      const agentId = data.agent_id;

      showToast.success("AI Job Application process started!");

      // Poll for status updates
      pollAgentStatus(agentId);
    } catch (error) {
      console.error("Job application error:", error);
      showToast.error("Failed to start job application process");
      setIsProcessing(false);
    }
  };

  const pollAgentStatus = async (agentId: string) => {
    const maxAttempts = 60; // 2 minutes max
    let attempts = 0;

    const poll = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/api/job-application/${agentId}/status`
        );
        if (!response.ok) throw new Error("Failed to get status");

        const data = await response.json();
        setAgentStatus(data.status);

        if (data.status.status === "completed") {
          // Get final results
          const resultsResponse = await fetch(
            `http://localhost:8000/api/job-application/${agentId}/results`
          );
          if (resultsResponse.ok) {
            const resultsData = await resultsResponse.json();
            setResults(resultsData.results);
          }
          setIsProcessing(false);
          showToast.success("Job application process completed!");
          return;
        } else if (data.status.status === "error") {
          setIsProcessing(false);
          showToast.error("Job application process failed");
          return;
        }

        attempts++;
        if (attempts < maxAttempts) {
          setTimeout(poll, 2000); // Poll every 2 seconds
        } else {
          setIsProcessing(false);
          showToast.error("Process timed out");
        }
      } catch (error) {
        console.error("Status poll error:", error);
        setIsProcessing(false);
        showToast.error("Failed to get status updates");
      }
    };

    poll();
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "initializing":
        return <Clock className="h-5 w-5 text-blue-500 animate-spin" />;
      case "parsing_resume":
        return <FileText className="h-5 w-5 text-orange-500 animate-pulse" />;
      case "searching_jobs":
        return <Search className="h-5 w-5 text-purple-500 animate-pulse" />;
      case "generating_cover_letters":
        return <Brain className="h-5 w-5 text-green-500 animate-pulse" />;
      case "completed":
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case "error":
        return <AlertCircle className="h-5 w-5 text-red-500" />;
      default:
        return <Clock className="h-5 w-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed":
        return "from-green-500 to-green-600";
      case "error":
        return "from-red-500 to-red-600";
      case "generating_cover_letters":
        return "from-green-500 to-green-600";
      case "searching_jobs":
        return "from-purple-500 to-purple-600";
      case "parsing_resume":
        return "from-orange-500 to-orange-600";
      default:
        return "from-blue-500 to-blue-600";
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
            <Brain className="h-8 w-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            AI Job Application Agent
          </h1>
          <p className="text-gray-600 dark:text-gray-300 text-lg">
            Upload your resume and let AI find perfect jobs and create
            personalized cover letters
          </p>
        </motion.div>

        {/* Resume Upload Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-gray-700 mb-8"
        >
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Step 1: Upload Your Resume
          </h2>

          <div className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center">
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileUpload}
              className="hidden"
              id="resume-upload"
            />
            <label
              htmlFor="resume-upload"
              className="cursor-pointer flex flex-col items-center"
            >
              <Upload className="h-12 w-12 text-gray-400 mb-4" />
              <p className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                Click to upload your resume
              </p>
              <p className="text-gray-600 dark:text-gray-300">
                PDF files only (max 10MB)
              </p>
            </label>
          </div>

          {resumeData && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-6 p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-700"
            >
              <div className="flex items-center mb-3">
                <CheckCircle className="h-5 w-5 text-green-500 mr-2" />
                <h3 className="font-semibold text-green-900 dark:text-green-100">
                  Resume Parsed Successfully
                </h3>
              </div>
              <div className="grid md:grid-cols-2 gap-4 text-sm">
                <div>
                  <p>
                    <span className="font-medium">Name:</span>{" "}
                    {resumeData.parsed_data.name}
                  </p>
                  <p>
                    <span className="font-medium">Experience:</span>{" "}
                    {resumeData.parsed_data.experience_level}
                  </p>
                  <p>
                    <span className="font-medium">Education:</span>{" "}
                    {resumeData.parsed_data.education}
                  </p>
                </div>
                <div>
                  <p>
                    <span className="font-medium">Skills:</span>{" "}
                    {resumeData.parsed_data.skills.slice(0, 3).join(", ")}...
                  </p>
                  <p>
                    <span className="font-medium">Years:</span>{" "}
                    {resumeData.parsed_data.years_experience}
                  </p>
                </div>
              </div>
            </motion.div>
          )}
        </motion.div>

        {/* AI Processing Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-gray-700 mb-8"
        >
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Step 2: AI Job Application Process
          </h2>

          <div className="flex justify-center mb-6">
            <motion.button
              onClick={startJobApplication}
              disabled={!resumeData || isProcessing}
              className="px-8 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg font-semibold text-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-3"
              whileHover={{ scale: resumeData && !isProcessing ? 1.05 : 1 }}
              whileTap={{ scale: resumeData && !isProcessing ? 0.95 : 1 }}
            >
              <Zap className="h-5 w-5" />
              <span>
                {isProcessing ? "Processing..." : "Start AI Job Search"}
              </span>
            </motion.button>
          </div>

          {/* Progress Section */}
          {agentStatus && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-4"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  {getStatusIcon(agentStatus.status)}
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">
                      {agentStatus.current_step}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-300">
                      Status: {agentStatus.status.replace("_", " ")}
                    </p>
                  </div>
                </div>
                <span className="text-sm font-medium text-gray-900 dark:text-white">
                  {agentStatus.progress}%
                </span>
              </div>

              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                <motion.div
                  className={`h-3 rounded-full bg-gradient-to-r ${getStatusColor(
                    agentStatus.status
                  )}`}
                  style={{ width: `${agentStatus.progress}%` }}
                  initial={{ width: 0 }}
                  animate={{ width: `${agentStatus.progress}%` }}
                  transition={{ duration: 0.5 }}
                />
              </div>
            </motion.div>
          )}
        </motion.div>

        {/* Results Section */}
        {results && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-gray-700"
          >
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
              Results: Your AI-Generated Applications
            </h2>

            <div className="grid md:grid-cols-3 gap-6 mb-8">
              <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                  {results.jobs_found}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-300">
                  Jobs Found
                </div>
              </div>
              <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
                <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                  {results.cover_letters?.length || 0}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-300">
                  Cover Letters
                </div>
              </div>
              <div className="text-center p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                  {Math.round(
                    results.matching_jobs?.reduce(
                      (acc: number, job: any) => acc + job.match_score,
                      0
                    ) / results.matching_jobs?.length
                  ) || 0}
                  %
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-300">
                  Avg Match
                </div>
              </div>
            </div>

            {/* Cover Letters */}
            {results.cover_letters && results.cover_letters.length > 0 && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Generated Cover Letters
                </h3>
                {results.cover_letters.map((letter: any, index: number) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="border border-gray-200 dark:border-gray-700 rounded-lg p-6"
                  >
                    <div className="flex items-center justify-between mb-4">
                      <div>
                        <h4 className="font-semibold text-gray-900 dark:text-white">
                          {letter.job_title} at {letter.company}
                        </h4>
                        <p className="text-sm text-gray-600 dark:text-gray-300">
                          Match Score: {letter.match_score}%
                        </p>
                      </div>
                      <div className="flex space-x-2">
                        <button className="p-2 text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white">
                          <Eye className="h-4 w-4" />
                        </button>
                        <button className="p-2 text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white">
                          <Download className="h-4 w-4" />
                        </button>
                      </div>
                    </div>
                    <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                      <p className="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-line line-clamp-6">
                        {letter.cover_letter}
                      </p>
                    </div>
                  </motion.div>
                ))}
              </div>
            )}
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default AIJobApplication;
