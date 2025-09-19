import React, { useState, useCallback } from "react";
import { motion } from "framer-motion";
import { Upload, FileText, CheckCircle, AlertCircle } from "lucide-react";
import { showToast } from "./Toast";

interface ResumeParseResult {
  skills_count?: number;
  experience_years?: number;
  success: boolean;
  message?: string;
}

interface ResumeUploadProps {
  resumeUploaded: boolean;
  setResumeUploaded: (uploaded: boolean) => void;
  onProcessComplete?: (result: ResumeParseResult) => void;
}

const ResumeUpload: React.FC<ResumeUploadProps> = ({
  resumeUploaded,
  setResumeUploaded,
  onProcessComplete,
}) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const processFile = useCallback(
    async (file: File) => {
      console.log("Processing file:", file.name);
      setIsProcessing(true);

      try {
        // Create FormData for file upload
        const formData = new FormData();
        formData.append("file", file);

        // Get token and verify it exists
        const token = localStorage.getItem("access_token"); // Fixed: use same key as AuthContext
        console.log("Token exists:", !!token);
        console.log("Token preview:", token?.substring(0, 20) + "...");

        if (!token) {
          throw new Error(
            "No authentication token found. Please sign in again."
          );
        }

        // Call the resume parsing API
        const response = await fetch(
          "http://localhost:8000/api/agents/parse-resume",
          {
            method: "POST",
            body: formData,
            headers: {
              Authorization: `Bearer ${token}`,
              // Don't set Content-Type when using FormData - let browser set it
            },
          }
        );

        console.log("Response status:", response.status);

        if (response.status === 401) {
          localStorage.removeItem("token"); // Clear invalid token
          throw new Error("Authentication failed. Please sign in again.");
        }

        if (!response.ok) {
          const errorText = await response.text();
          console.error("API Error:", errorText);
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log("Resume parsing result:", result);

        setResumeUploaded(true);
        setIsProcessing(false);

        // Show success with actual data from the agent
        if (result.skills_count) {
          showToast.success(
            `Resume parsed successfully! Found ${
              result.skills_count
            } relevant skills and ${
              result.experience_years || 0
            } years of experience.`
          );
        } else {
          showToast.success("Resume parsed successfully!");
        }

        // Trigger any callback to parent component
        if (typeof onProcessComplete === "function") {
          onProcessComplete(result);
        }
      } catch (error) {
        console.error("Resume processing failed:", error);
        setIsProcessing(false);

        // Show more specific error messages
        if (error instanceof Error) {
          if (error.message.includes("Authentication failed")) {
            showToast.error("Session expired. Please sign in again.");
            // Optionally redirect to sign in page
            window.location.href = "/signin";
          } else if (error.message.includes("No authentication token")) {
            showToast.error("Please sign in to upload your resume.");
            window.location.href = "/signin";
          } else {
            showToast.error(error.message);
          }
        } else {
          showToast.error(
            "Failed to process resume. Please try again or check if the file is a valid PDF."
          );
        }
      }
    },
    [setIsProcessing, setResumeUploaded, onProcessComplete]
  );

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragOver(false);

      const files = Array.from(e.dataTransfer.files);
      const pdfFile = files.find((file) => file.type === "application/pdf");

      if (pdfFile) {
        processFile(pdfFile);
      } else {
        showToast.error("Please upload a PDF file");
      }
    },
    [processFile]
  );

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      processFile(file);
    }
  };

  if (resumeUploaded && !isProcessing) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="bg-green-50 dark:bg-green-900/20 border-2 border-green-200 dark:border-green-800 rounded-xl p-6"
      >
        <div className="flex items-center space-x-4">
          <CheckCircle className="h-12 w-12 text-green-600 dark:text-green-400" />
          <div>
            <h3 className="text-lg font-semibold text-green-800 dark:text-green-200">
              Resume Parsed Successfully!
            </h3>
            <p className="text-green-600 dark:text-green-300">
              We've extracted your skills and are now finding matching jobs
            </p>
          </div>
        </div>

        <div className="mt-4 space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-green-700 dark:text-green-300">
              Skills extracted
            </span>
            <span className="font-medium text-green-800 dark:text-green-200">
              12
            </span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-green-700 dark:text-green-300">
              Experience level
            </span>
            <span className="font-medium text-green-800 dark:text-green-200">
              Senior
            </span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-green-700 dark:text-green-300">
              Years of experience
            </span>
            <span className="font-medium text-green-800 dark:text-green-200">
              5+
            </span>
          </div>
        </div>

        <button
          onClick={() => setResumeUploaded(false)}
          className="mt-4 text-sm text-green-600 dark:text-green-400 hover:text-green-700 dark:hover:text-green-300"
        >
          Upload different resume
        </button>
      </motion.div>
    );
  }

  if (isProcessing) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="bg-blue-50 dark:bg-blue-900/20 border-2 border-blue-200 dark:border-blue-800 rounded-xl p-6"
      >
        <div className="flex items-center space-x-4">
          <div className="relative">
            <AlertCircle className="h-12 w-12 text-blue-600 dark:text-blue-400 animate-pulse" />
            <div className="absolute inset-0 rounded-full border-4 border-blue-600 dark:border-blue-400 animate-spin border-t-transparent"></div>
          </div>
          <div>
            <h3 className="text-lg font-semibold text-blue-800 dark:text-blue-200">
              Processing Your Resume...
            </h3>
            <p className="text-blue-600 dark:text-blue-300">
              Our AI is analyzing your skills and experience
            </p>
          </div>
        </div>

        <div className="mt-4 space-y-3">
          {[
            "Parsing document structure...",
            "Extracting skills and qualifications...",
            "Analyzing experience level...",
            "Preparing job matches...",
          ].map((step, index) => (
            <div key={step} className="flex items-center space-x-2">
              <div
                className={`w-2 h-2 rounded-full ${
                  index < 2 ? "bg-blue-600" : "bg-gray-300 dark:bg-gray-600"
                } ${index === 2 ? "animate-pulse" : ""}`}
              ></div>
              <span className="text-sm text-blue-700 dark:text-blue-300">
                {step}
              </span>
            </div>
          ))}
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300 ${
        isDragOver
          ? "border-blue-500 bg-blue-50 dark:bg-blue-900/20"
          : "border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-800/50"
      }`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <div className="space-y-4">
        <div className="mx-auto w-16 h-16 bg-gradient-to-r from-blue-500 to-teal-500 rounded-full flex items-center justify-center">
          <Upload className="h-8 w-8 text-white" />
        </div>

        <div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            Upload Your Resume
          </h3>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            Drag and drop your PDF resume here, or click to browse
          </p>
        </div>

        <div className="flex items-center justify-center space-x-2 text-sm text-gray-500 dark:text-gray-400">
          <FileText className="h-4 w-4" />
          <span>PDF format recommended</span>
        </div>

        <input
          type="file"
          accept=".pdf"
          onChange={handleFileSelect}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        />

        <button className="inline-flex items-center px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
          Choose File
        </button>
      </div>
    </motion.div>
  );
};

export default ResumeUpload;
