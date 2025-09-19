import React, { useState } from "react";
import { motion } from "framer-motion";
import {
  User,
  Mail,
  Phone,
  MapPin,
  Camera,
  Award,
  TrendingUp,
  Star,
  Edit,
  Save,
  X,
  Briefcase,
  GraduationCap,
} from "lucide-react";
import { useAuth } from "../contexts/AuthContext";
import { showToast } from "../components/Toast";

const Profile: React.FC = () => {
  const { user } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  // Create editable profile data with proper user structure
  const [editedUser, setEditedUser] = useState({
    full_name: user?.full_name || "",
    email: user?.email || "",
    phone: user?.phone || "",
    location: user?.location || "",
    experience_level: user?.experience_level || "Mid-Level",
    desired_salary: user?.desired_salary || "",
    preferred_job_types: user?.preferred_job_types || [],
  });

  const handleSave = async () => {
    if (!user) return;

    setIsLoading(true);
    try {
      // TODO: Add API call to update profile
      setIsEditing(false);
      showToast.success("Profile updated successfully!");
    } catch (error) {
      console.error("Failed to update profile:", error);
      showToast.error("Failed to update profile");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    setEditedUser({
      full_name: user?.full_name || "",
      email: user?.email || "",
      phone: user?.phone || "",
      location: user?.location || "",
      experience_level: user?.experience_level || "Mid-Level",
      desired_salary: user?.desired_salary || "",
      preferred_job_types: user?.preferred_job_types || [],
    });
    setIsEditing(false);
  };

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading profile...</p>
        </div>
      </div>
    );
  }

  const achievements = [
    {
      name: "Quick Starter",
      description: "Uploaded resume within first day",
      earned: user.resume_uploaded,
    },
    {
      name: "Profile Complete",
      description: "Completed all profile sections",
      earned: !!(user.full_name && user.email && user.location),
    },
    {
      name: "Skills Master",
      description: "Added skills to profile",
      earned: user.skills.length > 0,
    },
    {
      name: "Education Added",
      description: "Added education information",
      earned: user.education.length > 0,
    },
    {
      name: "Work Experience",
      description: "Added work experience",
      earned: user.work_experience.length > 0,
    },
    {
      name: "Professional",
      description: "Completed full profile",
      earned:
        user.skills.length > 0 &&
        user.education.length > 0 &&
        user.work_experience.length > 0,
    },
  ];

  const earnedAchievements = achievements.filter((a) => a.earned).length;
  const profileCompleteness = Math.round(
    (earnedAchievements / achievements.length) * 100
  );

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Profile
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Manage your account and track your progress
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Profile Card */}
          <div className="lg:col-span-1">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6"
            >
              <div className="text-center mb-6">
                <div className="relative inline-block">
                  <div className="w-24 h-24 bg-gradient-to-r from-blue-500 to-teal-500 rounded-full flex items-center justify-center text-white text-2xl font-bold mb-4">
                    {user.full_name
                      .split(" ")
                      .map((n) => n[0])
                      .join("")
                      .toUpperCase()}
                  </div>
                  <button className="absolute -bottom-2 -right-2 w-8 h-8 bg-white dark:bg-gray-700 rounded-full shadow-lg flex items-center justify-center border border-gray-200 dark:border-gray-600">
                    <Camera className="h-4 w-4 text-gray-600 dark:text-gray-300" />
                  </button>
                </div>

                <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                  {user.full_name}
                </h2>
                <p className="text-gray-600 dark:text-gray-300">{user.email}</p>

                <div className="flex items-center justify-center space-x-2 mt-4">
                  <div className="flex items-center space-x-1">
                    <Star className="h-4 w-4 text-yellow-400" />
                    <span className="text-sm font-medium text-gray-900 dark:text-white">
                      {user.experience_level}
                    </span>
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-600 dark:text-gray-300">
                      Profile Strength
                    </span>
                    <span className="text-sm font-medium text-gray-900 dark:text-white">
                      {profileCompleteness}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div
                      className="bg-gradient-to-r from-blue-500 to-teal-500 h-2 rounded-full"
                      style={{ width: `${profileCompleteness}%` }}
                    ></div>
                  </div>
                </div>

                <div className="text-sm space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600 dark:text-gray-300">
                      Skills
                    </span>
                    <span className="font-medium text-gray-900 dark:text-white">
                      {user.skills.length}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600 dark:text-gray-300">
                      Education
                    </span>
                    <span className="font-medium text-gray-900 dark:text-white">
                      {user.education.length}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600 dark:text-gray-300">
                      Work Experience
                    </span>
                    <span className="font-medium text-gray-900 dark:text-white">
                      {user.work_experience.length}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600 dark:text-gray-300">
                      Resume Uploaded
                    </span>
                    <span className="font-medium text-gray-900 dark:text-white">
                      {user.resume_uploaded ? "Yes" : "No"}
                    </span>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>

          {/* Profile Details */}
          <div className="lg:col-span-2 space-y-6">
            {/* Basic Information */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700"
            >
              <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    Basic Information
                  </h3>
                  {isEditing ? (
                    <div className="flex space-x-2">
                      <button
                        onClick={handleSave}
                        disabled={isLoading}
                        className="inline-flex items-center px-3 py-1 bg-green-600 text-white rounded-md text-sm hover:bg-green-700 disabled:opacity-50"
                      >
                        <Save className="h-4 w-4 mr-1" />
                        {isLoading ? "Saving..." : "Save"}
                      </button>
                      <button
                        onClick={handleCancel}
                        className="inline-flex items-center px-3 py-1 bg-gray-600 text-white rounded-md text-sm hover:bg-gray-700"
                      >
                        <X className="h-4 w-4 mr-1" />
                        Cancel
                      </button>
                    </div>
                  ) : (
                    <button
                      onClick={() => setIsEditing(true)}
                      className="inline-flex items-center px-3 py-1 bg-blue-600 text-white rounded-md text-sm hover:bg-blue-700"
                    >
                      <Edit className="h-4 w-4 mr-1" />
                      Edit
                    </button>
                  )}
                </div>
              </div>

              <div className="p-6">
                <div className="grid md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        <User className="h-4 w-4 inline mr-2" />
                        Full Name
                      </label>
                      {isEditing ? (
                        <input
                          type="text"
                          value={editedUser.full_name}
                          onChange={(e) =>
                            setEditedUser((prev) => ({
                              ...prev,
                              full_name: e.target.value,
                            }))
                          }
                          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                        />
                      ) : (
                        <p className="text-gray-900 dark:text-white">
                          {user.full_name}
                        </p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        <Mail className="h-4 w-4 inline mr-2" />
                        Email
                      </label>
                      <p className="text-gray-900 dark:text-white">
                        {user.email}
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                        Email cannot be changed
                      </p>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Experience Level
                      </label>
                      {isEditing ? (
                        <select
                          value={editedUser.experience_level}
                          onChange={(e) =>
                            setEditedUser((prev) => ({
                              ...prev,
                              experience_level: e.target.value,
                            }))
                          }
                          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                        >
                          <option value="Entry-Level">Entry-Level</option>
                          <option value="Mid-Level">Mid-Level</option>
                          <option value="Senior-Level">Senior-Level</option>
                          <option value="Executive">Executive</option>
                        </select>
                      ) : (
                        <p className="text-gray-900 dark:text-white">
                          {user.experience_level}
                        </p>
                      )}
                    </div>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        <Phone className="h-4 w-4 inline mr-2" />
                        Phone
                      </label>
                      {isEditing ? (
                        <input
                          type="tel"
                          value={editedUser.phone || ""}
                          onChange={(e) =>
                            setEditedUser((prev) => ({
                              ...prev,
                              phone: e.target.value,
                            }))
                          }
                          placeholder="Enter your phone number"
                          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                        />
                      ) : (
                        <p className="text-gray-900 dark:text-white">
                          {user.phone || "Not provided"}
                        </p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        <MapPin className="h-4 w-4 inline mr-2" />
                        Location
                      </label>
                      {isEditing ? (
                        <input
                          type="text"
                          value={editedUser.location || ""}
                          onChange={(e) =>
                            setEditedUser((prev) => ({
                              ...prev,
                              location: e.target.value,
                            }))
                          }
                          placeholder="Enter your location"
                          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                        />
                      ) : (
                        <p className="text-gray-900 dark:text-white">
                          {user.location || "Not provided"}
                        </p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Desired Salary
                      </label>
                      {isEditing ? (
                        <input
                          type="text"
                          value={editedUser.desired_salary || ""}
                          onChange={(e) =>
                            setEditedUser((prev) => ({
                              ...prev,
                              desired_salary: e.target.value,
                            }))
                          }
                          placeholder="e.g., $50,000 - $60,000"
                          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                        />
                      ) : (
                        <p className="text-gray-900 dark:text-white">
                          {user.desired_salary || "Not specified"}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Skills Section */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700"
            >
              <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                  <Briefcase className="h-5 w-5 mr-2 text-blue-500" />
                  Skills ({user.skills.length})
                </h3>
              </div>

              <div className="p-6">
                {user.skills.length > 0 ? (
                  <div className="grid gap-4">
                    {user.skills.map((skill, index) => (
                      <div
                        key={index}
                        className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-900 rounded-lg"
                      >
                        <div>
                          <h4 className="font-medium text-gray-900 dark:text-white">
                            {skill.skill_name}
                          </h4>
                          <p className="text-sm text-gray-600 dark:text-gray-300">
                            {skill.proficiency_level} • {skill.years_experience}{" "}
                            years
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <Briefcase className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-500 dark:text-gray-400">
                      No skills added yet. Upload a resume to automatically
                      extract your skills.
                    </p>
                  </div>
                )}
              </div>
            </motion.div>

            {/* Education Section */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.15 }}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700"
            >
              <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                  <GraduationCap className="h-5 w-5 mr-2 text-green-500" />
                  Education ({user.education.length})
                </h3>
              </div>

              <div className="p-6">
                {user.education.length > 0 ? (
                  <div className="space-y-4">
                    {user.education.map((edu, index) => (
                      <div
                        key={index}
                        className="p-4 bg-gray-50 dark:bg-gray-900 rounded-lg"
                      >
                        <h4 className="font-medium text-gray-900 dark:text-white">
                          {edu.degree} in {edu.field_of_study}
                        </h4>
                        <p className="text-gray-600 dark:text-gray-300">
                          {edu.institution_name}
                        </p>
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                          {edu.start_date} -{" "}
                          {edu.is_current ? "Present" : edu.end_date}
                          {edu.gpa && ` • GPA: ${edu.gpa}`}
                        </p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <GraduationCap className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-500 dark:text-gray-400">
                      No education information added yet.
                    </p>
                  </div>
                )}
              </div>
            </motion.div>

            {/* Work Experience Section */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700"
            >
              <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                  <Briefcase className="h-5 w-5 mr-2 text-purple-500" />
                  Work Experience ({user.work_experience.length})
                </h3>
              </div>

              <div className="p-6">
                {user.work_experience.length > 0 ? (
                  <div className="space-y-4">
                    {user.work_experience.map((work, index) => (
                      <div
                        key={index}
                        className="p-4 bg-gray-50 dark:bg-gray-900 rounded-lg"
                      >
                        <h4 className="font-medium text-gray-900 dark:text-white">
                          {work.job_title}
                        </h4>
                        <p className="text-gray-600 dark:text-gray-300">
                          {work.company_name}
                        </p>
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                          {work.start_date} -{" "}
                          {work.is_current ? "Present" : work.end_date}
                          {work.location && ` • ${work.location}`}
                        </p>
                        {work.description && (
                          <p className="text-sm text-gray-600 dark:text-gray-300 mt-2">
                            {work.description}
                          </p>
                        )}
                        {work.salary && (
                          <p className="text-sm text-green-600 dark:text-green-400 mt-1">
                            Salary: {work.salary}
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <Briefcase className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-500 dark:text-gray-400">
                      No work experience added yet.
                    </p>
                  </div>
                )}
              </div>
            </motion.div>

            {/* Achievements */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.25 }}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700"
            >
              <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                  <Award className="h-5 w-5 mr-2 text-yellow-500" />
                  Achievements ({earnedAchievements}/{achievements.length})
                </h3>
              </div>

              <div className="p-6">
                <div className="grid md:grid-cols-2 gap-4">
                  {achievements.map((achievement, index) => (
                    <div
                      key={index}
                      className={`p-4 rounded-lg border ${
                        achievement.earned
                          ? "bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800"
                          : "bg-gray-50 dark:bg-gray-900 border-gray-200 dark:border-gray-700"
                      }`}
                    >
                      <div className="flex items-start space-x-3">
                        <div
                          className={`w-8 h-8 rounded-full flex items-center justify-center ${
                            achievement.earned ? "bg-yellow-500" : "bg-gray-400"
                          }`}
                        >
                          <Award className="h-4 w-4 text-white" />
                        </div>
                        <div className="flex-1">
                          <h4
                            className={`font-medium ${
                              achievement.earned
                                ? "text-yellow-800 dark:text-yellow-200"
                                : "text-gray-600 dark:text-gray-400"
                            }`}
                          >
                            {achievement.name}
                          </h4>
                          <p
                            className={`text-sm ${
                              achievement.earned
                                ? "text-yellow-600 dark:text-yellow-300"
                                : "text-gray-500 dark:text-gray-500"
                            }`}
                          >
                            {achievement.description}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
