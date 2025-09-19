import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Briefcase, TrendingUp, Clock, Award } from "lucide-react";
import { useAuth } from "../contexts/AuthContext";
import ResumeUpload from "../components/ResumeUpload";
import JobCard from "../components/JobCard";
import JobDetailsModal from "../components/JobDetailsModal";
import { showToast } from "../components/Toast";

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

// Mock job data
const mockJobs: Job[] = [
  {
    id: "1",
    title: "Senior Frontend Developer",
    company: "TechCorp",
    logo: "💻",
    location: "San Francisco, CA",
    description: "Build amazing user experiences with React and TypeScript",
    matchScore: 95,
    applied: false,
    salary: "$120k - $150k",
    type: "Full-time",
  },
  {
    id: "2",
    title: "Full Stack Engineer",
    company: "StartupXYZ",
    logo: "🚀",
    location: "New York, NY",
    description: "Join our dynamic team building the next generation platform",
    matchScore: 88,
    applied: true,
    salary: "$100k - $130k",
    type: "Full-time",
  },
  {
    id: "3",
    title: "React Developer",
    company: "WebSolutions",
    logo: "⚛️",
    location: "Remote",
    description:
      "Create responsive web applications using modern React patterns",
    matchScore: 82,
    applied: false,
    salary: "$90k - $110k",
    type: "Contract",
  },
];

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [isJobModalOpen, setIsJobModalOpen] = useState(false);
  const [sortBy, setSortBy] = useState<"match" | "recent">("match");
  const [filterApplied, setFilterApplied] = useState<
    "all" | "applied" | "not-applied"
  >("all");
  const [jobs, setJobs] = useState<Job[]>([]);
  const [resumeUploaded, setResumeUploaded] = useState(false);
  const [isLoadingJobs, setIsLoadingJobs] = useState(false);

  // Handle resume processing completion
  const handleResumeProcessComplete = async (result: {
    skills_count?: number;
    experience_years?: number;
    success: boolean;
    message?: string;
  }) => {
    console.log("Resume processing completed:", result);
    setIsLoadingJobs(true);

    try {
      // Fetch real jobs from the backend after resume is processed
      const response = await fetch(
        "http://localhost:8000/api/agents/find-jobs",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        }
      );

      if (response.ok) {
        const jobData = await response.json();
        console.log("Jobs found:", jobData);

        // Update jobs with real data from the agent
        if (jobData.jobs && jobData.jobs.length > 0) {
          setJobs(jobData.jobs);
          showToast.success(`Found ${jobData.jobs.length} matching jobs!`);
        } else {
          // Fallback to mock data if no real jobs found
          setJobs(mockJobs);
          showToast.info("Using sample jobs for demonstration.");
        }
      } else {
        // Fallback to mock data on API error
        setJobs(mockJobs);
        showToast.info("Using sample jobs. Check backend connection.");
      }
    } catch (error) {
      console.error("Error fetching jobs:", error);
      setJobs(mockJobs);
      showToast.error("Failed to fetch jobs. Using sample data.");
    } finally {
      setIsLoadingJobs(false);
    }
  };

  useEffect(() => {
    // Initialize with mock jobs
    setJobs(mockJobs);
    if (user?.resume_uploaded) {
      setResumeUploaded(true);
    }
  }, [user?.resume_uploaded]);

  const filteredAndSortedJobs = jobs
    .filter((job) => {
      if (filterApplied === "applied") return job.applied;
      if (filterApplied === "not-applied") return !job.applied;
      return true;
    })
    .sort((a, b) => {
      if (sortBy === "match") return b.matchScore - a.matchScore;
      return a.title.localeCompare(b.title);
    });

  useEffect(() => {
    if (resumeUploaded && jobs.length > 0) {
      // Simulate job matching
      setTimeout(() => {
        showToast.info(`Found ${jobs.length} jobs matching your profile!`);
      }, 1000);
    }
  }, [resumeUploaded, jobs.length]);

  const handleViewJobDetails = (job: Job) => {
    setSelectedJob(job);
    setIsJobModalOpen(true);
  };

  const handleApplyToJob = async (jobId: string) => {
    const job = jobs.find((j) => j.id === jobId);
    if (!job) return;

    try {
      const response = await fetch(
        "http://localhost:8000/api/agents/apply-to-job",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
          body: JSON.stringify({
            job_id: jobId,
            job_title: job.title,
            company: job.company,
          }),
        }
      );

      if (response.ok) {
        const result = await response.json();
        console.log("Application result:", result);

        // Update the job as applied
        setJobs((prevJobs) =>
          prevJobs.map((j) => (j.id === jobId ? { ...j, applied: true } : j))
        );

        showToast.success(
          `Successfully applied to ${job.title} at ${job.company}!`
        );
      } else {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error("Job application failed:", error);
      showToast.error("Failed to apply to job. Please try again.");
    }
  };

  const stats = [
    {
      label: "Applications Submitted",
      value: jobs.filter((job) => job.applied).length,
      icon: Briefcase,
      color: "from-blue-500 to-blue-600",
      change: "+2 this week",
    },
    {
      label: "Average Match Score",
      value:
        jobs.length > 0
          ? Math.round(
              jobs.reduce((acc, job) => acc + job.matchScore, 0) / jobs.length
            ) + "%"
          : "0%",
      icon: TrendingUp,
      color: "from-teal-500 to-teal-600",
      change: "+12% from last month",
    },
    {
      label: "Profile Level",
      value: user?.experience_level || "Entry Level",
      icon: Award,
      color: "from-purple-500 to-purple-600",
      change: "Professional level",
    },
    {
      label: "Jobs Found",
      value: jobs.length,
      icon: Clock,
      color: "from-orange-500 to-orange-600",
      change: "Updated 5 min ago",
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                  Welcome back, {user?.full_name}! 👋
                </h1>
                <p className="text-gray-600 dark:text-gray-300 mt-1">
                  Your AI agents are working to find the perfect opportunities
                  for you.
                </p>
              </div>

              {user && user.skills.length > 0 && (
                <div className="flex items-center space-x-2">
                  <Award className="h-5 w-5 text-blue-500" />
                  <div className="flex space-x-1">
                    {user.skills.slice(0, 3).map((skill, index) => (
                      <span
                        key={index}
                        className="px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-xs rounded-md"
                      >
                        {skill.skill_name}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </motion.div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-gray-700"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {stat.label}
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">
                    {stat.value}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {stat.change}
                  </p>
                </div>
                <div
                  className={`w-12 h-12 rounded-lg bg-gradient-to-r ${stat.color} flex items-center justify-center`}
                >
                  <stat.icon className="h-6 w-6 text-white" />
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Resume Upload Section */}
          <div className="lg:col-span-1">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="sticky top-8"
            >
              <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-gray-700 mb-6">
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                  Resume Analysis
                </h2>
                <ResumeUpload
                  resumeUploaded={resumeUploaded}
                  setResumeUploaded={setResumeUploaded}
                  onProcessComplete={handleResumeProcessComplete}
                />
              </div>

              {resumeUploaded && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-gray-700"
                >
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                    Profile Strength
                  </h3>
                  <div className="space-y-4">
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm text-gray-600 dark:text-gray-300">
                          Skills Match
                        </span>
                        <span className="text-sm font-medium text-gray-900 dark:text-white">
                          92%
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div
                          className="bg-gradient-to-r from-green-500 to-green-600 h-2 rounded-full"
                          style={{ width: "92%" }}
                        ></div>
                      </div>
                    </div>

                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm text-gray-600 dark:text-gray-300">
                          Experience Level
                        </span>
                        <span className="text-sm font-medium text-gray-900 dark:text-white">
                          95%
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div
                          className="bg-gradient-to-r from-blue-500 to-blue-600 h-2 rounded-full"
                          style={{ width: "95%" }}
                        ></div>
                      </div>
                    </div>

                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm text-gray-600 dark:text-gray-300">
                          Profile Completeness
                        </span>
                        <span className="text-sm font-medium text-gray-900 dark:text-white">
                          88%
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div
                          className="bg-gradient-to-r from-purple-500 to-purple-600 h-2 rounded-full"
                          style={{ width: "88%" }}
                        ></div>
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}
            </motion.div>
          </div>

          {/* Jobs Section */}
          <div className="lg:col-span-2">
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
            >
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                    Matching Jobs
                  </h2>
                  <p className="text-gray-600 dark:text-gray-300">
                    {filteredAndSortedJobs.length} positions found
                  </p>
                </div>

                <div className="flex items-center space-x-3">
                  <select
                    value={sortBy}
                    onChange={(e) =>
                      setSortBy(e.target.value as "match" | "recent")
                    }
                    className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm"
                  >
                    <option value="match">Sort by Match</option>
                    <option value="recent">Sort by Recent</option>
                  </select>

                  <select
                    value={filterApplied}
                    onChange={(e) =>
                      setFilterApplied(
                        e.target.value as "all" | "applied" | "not-applied"
                      )
                    }
                    className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm"
                  >
                    <option value="all">All Jobs</option>
                    <option value="not-applied">Not Applied</option>
                    <option value="applied">Applied</option>
                  </select>
                </div>
              </div>

              {resumeUploaded ? (
                <div className="space-y-4">
                  {isLoadingJobs ? (
                    <div className="text-center py-8">
                      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                      <p className="mt-4 text-gray-600 dark:text-gray-400">
                        Finding jobs that match your profile...
                      </p>
                    </div>
                  ) : (
                    filteredAndSortedJobs.map((job, index) => (
                      <motion.div
                        key={job.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                      >
                        <JobCard
                          job={job}
                          onViewDetails={handleViewJobDetails}
                          onApply={handleApplyToJob}
                        />
                      </motion.div>
                    ))
                  )}
                </div>
              ) : (
                <div className="text-center py-12">
                  <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center">
                    <Briefcase className="h-8 w-8 text-gray-400" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    Upload your resume to see matching jobs
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300">
                    Our AI will analyze your skills and find the perfect
                    opportunities
                  </p>
                </div>
              )}
            </motion.div>
          </div>
        </div>
      </div>

      <JobDetailsModal
        job={selectedJob}
        isOpen={isJobModalOpen}
        onClose={() => {
          setIsJobModalOpen(false);
          setSelectedJob(null);
        }}
        onApply={handleApplyToJob}
      />
    </div>
  );
};

export default Dashboard;
