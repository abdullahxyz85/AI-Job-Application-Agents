import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Bell, 
  Moon, 
  Sun, 
  Globe, 
  Shield, 
  Key, 
  Database,
  Mail,
  Smartphone,
  Check,
  ExternalLink
} from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';
import { showToast } from '../components/Toast';

const Settings: React.FC = () => {
  const { theme, toggleTheme } = useTheme();
  const [notifications, setNotifications] = useState({
    email: true,
    push: false,
    jobMatches: true,
    applicationUpdates: true,
    weeklyDigest: true
  });
  const [preferences, setPreferences] = useState({
    autoApply: false,
    coverLetterApproval: true,
    jobTypes: ['Full-time', 'Contract'],
    salaryRange: { min: 80000, max: 150000 }
  });

  const handleNotificationChange = (key: string, value: boolean) => {
    setNotifications(prev => ({ ...prev, [key]: value }));
    showToast.success('Notification settings updated');
  };

  const handlePreferenceChange = (key: string, value: any) => {
    setPreferences(prev => ({ ...prev, [key]: value }));
    showToast.success('Preferences updated');
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Settings
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Customize your AI job search experience
          </p>
        </motion.div>

        <div className="space-y-8">
          {/* Appearance */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700"
          >
            <div className="p-6 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                <Globe className="h-5 w-5 mr-2 text-blue-500" />
                Appearance
              </h2>
            </div>

            <div className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-medium text-gray-900 dark:text-white">Theme</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-300">
                    Choose your preferred color scheme
                  </p>
                </div>
                <button
                  onClick={toggleTheme}
                  className="flex items-center space-x-2 px-4 py-2 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                >
                  {theme === 'light' ? (
                    <>
                      <Moon className="h-4 w-4" />
                      <span>Dark Mode</span>
                    </>
                  ) : (
                    <>
                      <Sun className="h-4 w-4" />
                      <span>Light Mode</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </motion.div>

          {/* Notifications */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700"
          >
            <div className="p-6 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                <Bell className="h-5 w-5 mr-2 text-blue-500" />
                Notifications
              </h2>
            </div>

            <div className="p-6 space-y-4">
              {[
                {
                  key: 'email',
                  icon: Mail,
                  title: 'Email Notifications',
                  description: 'Get updates via email'
                },
                {
                  key: 'push',
                  icon: Smartphone,
                  title: 'Push Notifications',
                  description: 'Browser notifications for real-time updates'
                },
                {
                  key: 'jobMatches',
                  icon: Check,
                  title: 'Job Matches',
                  description: 'Notify me when new matching jobs are found'
                },
                {
                  key: 'applicationUpdates',
                  icon: Check,
                  title: 'Application Updates',
                  description: 'Updates on application status and responses'
                },
                {
                  key: 'weeklyDigest',
                  icon: Check,
                  title: 'Weekly Digest',
                  description: 'Weekly summary of activity and opportunities'
                }
              ].map(({ key, icon: Icon, title, description }) => (
                <div key={key} className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <Icon className="h-5 w-5 text-gray-400" />
                    <div>
                      <h3 className="font-medium text-gray-900 dark:text-white">
                        {title}
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-300">
                        {description}
                      </p>
                    </div>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={notifications[key as keyof typeof notifications]}
                      onChange={(e) => handleNotificationChange(key, e.target.checked)}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                  </label>
                </div>
              ))}
            </div>
          </motion.div>

          {/* AI Agent Preferences */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700"
          >
            <div className="p-6 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                <Shield className="h-5 w-5 mr-2 text-blue-500" />
                AI Agent Preferences
              </h2>
            </div>

            <div className="p-6 space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-medium text-gray-900 dark:text-white">Auto Apply</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-300">
                    Automatically apply to jobs that match 90%+
                  </p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={preferences.autoApply}
                    onChange={(e) => handlePreferenceChange('autoApply', e.target.checked)}
                    className="sr-only peer"
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                </label>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-medium text-gray-900 dark:text-white">Cover Letter Approval</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-300">
                    Require approval before submitting cover letters
                  </p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={preferences.coverLetterApproval}
                    onChange={(e) => handlePreferenceChange('coverLetterApproval', e.target.checked)}
                    className="sr-only peer"
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                </label>
              </div>

              <div>
                <h3 className="font-medium text-gray-900 dark:text-white mb-3">Job Types</h3>
                <div className="space-y-2">
                  {['Full-time', 'Part-time', 'Contract', 'Internship'].map((type) => (
                    <label key={type} className="flex items-center">
                      <input
                        type="checkbox"
                        checked={preferences.jobTypes.includes(type)}
                        onChange={(e) => {
                          const newTypes = e.target.checked
                            ? [...preferences.jobTypes, type]
                            : preferences.jobTypes.filter(t => t !== type);
                          handlePreferenceChange('jobTypes', newTypes);
                        }}
                        className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
                      />
                      <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">
                        {type}
                      </span>
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <h3 className="font-medium text-gray-900 dark:text-white mb-3">Salary Range</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm text-gray-600 dark:text-gray-300 mb-1">
                      Minimum
                    </label>
                    <input
                      type="number"
                      value={preferences.salaryRange.min}
                      onChange={(e) => handlePreferenceChange('salaryRange', {
                        ...preferences.salaryRange,
                        min: parseInt(e.target.value)
                      })}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-sm text-gray-600 dark:text-gray-300 mb-1">
                      Maximum
                    </label>
                    <input
                      type="number"
                      value={preferences.salaryRange.max}
                      onChange={(e) => handlePreferenceChange('salaryRange', {
                        ...preferences.salaryRange,
                        max: parseInt(e.target.value)
                      })}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                    />
                  </div>
                </div>
              </div>
            </div>
          </motion.div>

          {/* API Connections */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700"
          >
            <div className="p-6 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                <Database className="h-5 w-5 mr-2 text-blue-500" />
                API Connections
              </h2>
            </div>

            <div className="p-6 space-y-4">
              {[
                { name: 'LinkedIn', status: 'Connected', color: 'green' },
                { name: 'Indeed', status: 'Not Connected', color: 'gray' },
                { name: 'Glassdoor', status: 'Connected', color: 'green' },
                { name: 'AngelList', status: 'Not Connected', color: 'gray' }
              ].map((connection) => (
                <div key={connection.name} className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className={`w-3 h-3 rounded-full ${
                      connection.color === 'green' ? 'bg-green-500' : 'bg-gray-400'
                    }`}></div>
                    <div>
                      <h3 className="font-medium text-gray-900 dark:text-white">
                        {connection.name}
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-300">
                        {connection.status}
                      </p>
                    </div>
                  </div>
                  <button className="inline-flex items-center px-3 py-1 border border-gray-300 dark:border-gray-600 rounded-md text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700">
                    {connection.status === 'Connected' ? 'Disconnect' : 'Connect'}
                    <ExternalLink className="h-3 w-3 ml-1" />
                  </button>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Security */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700"
          >
            <div className="p-6 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                <Key className="h-5 w-5 mr-2 text-blue-500" />
                Security
              </h2>
            </div>

            <div className="p-6 space-y-4">
              <button className="w-full flex items-center justify-between p-4 border border-gray-200 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                <div className="text-left">
                  <h3 className="font-medium text-gray-900 dark:text-white">
                    Change Password
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-300">
                    Update your password to keep your account secure
                  </p>
                </div>
                <ExternalLink className="h-4 w-4 text-gray-400" />
              </button>

              <button className="w-full flex items-center justify-between p-4 border border-gray-200 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                <div className="text-left">
                  <h3 className="font-medium text-gray-900 dark:text-white">
                    Download Data
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-300">
                    Download a copy of your data and application history
                  </p>
                </div>
                <ExternalLink className="h-4 w-4 text-gray-400" />
              </button>

              <button className="w-full flex items-center justify-between p-4 border border-red-200 dark:border-red-800 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors text-red-600 dark:text-red-400">
                <div className="text-left">
                  <h3 className="font-medium">Delete Account</h3>
                  <p className="text-sm">Permanently delete your account and all data</p>
                </div>
                <ExternalLink className="h-4 w-4" />
              </button>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default Settings;