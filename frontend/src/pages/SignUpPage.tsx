import React, { useState } from "react";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import {
  Mail,
  Lock,
  Eye,
  EyeOff,
  User,
  UserPlus,
  ArrowRight,
  Brain,
  Check,
} from "lucide-react";
import { useAuth } from "../contexts/AuthContext";

const SignUpPage: React.FC = () => {
  const { signUp } = useAuth();
  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.fullName) {
      newErrors.fullName = "Full name is required";
    } else if (formData.fullName.length < 2) {
      newErrors.fullName = "Full name must be at least 2 characters";
    }

    if (!formData.email) {
      newErrors.email = "Email is required";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "Please enter a valid email";
    }

    if (!formData.password) {
      newErrors.password = "Password is required";
    } else if (formData.password.length < 6) {
      newErrors.password = "Password must be at least 6 characters";
    }

    if (!formData.confirmPassword) {
      newErrors.confirmPassword = "Please confirm your password";
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = "Passwords do not match";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) return;

    setIsLoading(true);
    try {
      const success = await signUp({
        full_name: formData.fullName,
        email: formData.email,
        password: formData.password,
      });
      if (success) {
        // Redirect will be handled by App component based on auth state
      }
    } catch (error) {
      console.error("Sign up error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: "" }));
    }
  };

  const getPasswordStrength = (password: string) => {
    let strength = 0;
    if (password.length >= 6) strength += 1;
    if (password.match(/[a-z]/) && password.match(/[A-Z]/)) strength += 1;
    if (password.match(/\d/)) strength += 1;
    if (password.match(/[^a-zA-Z\d]/)) strength += 1;
    return strength;
  };

  const passwordStrength = getPasswordStrength(formData.password);
  const getStrengthColor = (strength: number) => {
    if (strength < 2) return "bg-red-500";
    if (strength < 3) return "bg-yellow-500";
    return "bg-green-500";
  };

  const getStrengthText = (strength: number) => {
    if (strength < 2) return "Weak";
    if (strength < 3) return "Medium";
    return "Strong";
  };

  return (
    <div className="min-h-screen flex">
      {/* Left Side - Branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-purple-600 via-blue-600 to-indigo-700 relative overflow-hidden">
        <div className="absolute inset-0 bg-black opacity-20"></div>
        <div className="relative z-10 flex flex-col justify-center items-center p-12 text-white">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center"
          >
            <div className="w-20 h-20 mx-auto mb-6 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
              <Brain className="h-10 w-10 text-white" />
            </div>
            <h1 className="text-4xl font-bold mb-4">Join AI Job Agent</h1>
            <p className="text-xl mb-8 text-blue-100">
              Start your AI-powered career journey today
            </p>
            <div className="space-y-4 text-left max-w-md">
              <div className="flex items-center space-x-3">
                <Check className="h-5 w-5 text-green-300" />
                <span>Free account setup</span>
              </div>
              <div className="flex items-center space-x-3">
                <Check className="h-5 w-5 text-green-300" />
                <span>Personalized job recommendations</span>
              </div>
              <div className="flex items-center space-x-3">
                <Check className="h-5 w-5 text-green-300" />
                <span>AI-generated cover letters</span>
              </div>
              <div className="flex items-center space-x-3">
                <Check className="h-5 w-5 text-green-300" />
                <span>Application tracking dashboard</span>
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Right Side - Sign Up Form */}
      <div className="w-full lg:w-1/2 flex flex-col justify-center px-6 py-12 lg:px-8 bg-gray-50 dark:bg-gray-900">
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6 }}
          className="sm:mx-auto sm:w-full sm:max-w-md"
        >
          {/* Mobile Logo */}
          <div className="lg:hidden text-center mb-8">
            <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-purple-500 to-blue-600 rounded-full flex items-center justify-center">
              <Brain className="h-8 w-8 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              AI Job Agent
            </h2>
          </div>

          <div className="bg-white dark:bg-gray-800 py-8 px-6 shadow-xl rounded-lg border border-gray-200 dark:border-gray-700">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
                Create your account
              </h2>
              <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                Join thousands of job seekers using AI to land their dream job
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Full Name Field */}
              <div>
                <label htmlFor="fullName" className="sr-only">
                  Full name
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <User className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="fullName"
                    name="fullName"
                    type="text"
                    autoComplete="name"
                    required
                    value={formData.fullName}
                    onChange={handleInputChange}
                    className={`appearance-none relative block w-full pl-10 pr-3 py-3 border ${
                      errors.fullName
                        ? "border-red-300 dark:border-red-600"
                        : "border-gray-300 dark:border-gray-600"
                    } placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white bg-white dark:bg-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 dark:focus:border-purple-400 transition-colors duration-200`}
                    placeholder="Full name"
                  />
                </div>
                {errors.fullName && (
                  <p className="mt-2 text-sm text-red-600 dark:text-red-400">
                    {errors.fullName}
                  </p>
                )}
              </div>

              {/* Email Field */}
              <div>
                <label htmlFor="email" className="sr-only">
                  Email address
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Mail className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="email"
                    name="email"
                    type="email"
                    autoComplete="email"
                    required
                    value={formData.email}
                    onChange={handleInputChange}
                    className={`appearance-none relative block w-full pl-10 pr-3 py-3 border ${
                      errors.email
                        ? "border-red-300 dark:border-red-600"
                        : "border-gray-300 dark:border-gray-600"
                    } placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white bg-white dark:bg-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 dark:focus:border-purple-400 transition-colors duration-200`}
                    placeholder="Email address"
                  />
                </div>
                {errors.email && (
                  <p className="mt-2 text-sm text-red-600 dark:text-red-400">
                    {errors.email}
                  </p>
                )}
              </div>

              {/* Password Field */}
              <div>
                <label htmlFor="password" className="sr-only">
                  Password
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Lock className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="password"
                    name="password"
                    type={showPassword ? "text" : "password"}
                    autoComplete="new-password"
                    required
                    value={formData.password}
                    onChange={handleInputChange}
                    className={`appearance-none relative block w-full pl-10 pr-10 py-3 border ${
                      errors.password
                        ? "border-red-300 dark:border-red-600"
                        : "border-gray-300 dark:border-gray-600"
                    } placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white bg-white dark:bg-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 dark:focus:border-purple-400 transition-colors duration-200`}
                    placeholder="Password"
                  />
                  <button
                    type="button"
                    className="absolute inset-y-0 right-0 pr-3 flex items-center"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? (
                      <EyeOff className="h-5 w-5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300" />
                    ) : (
                      <Eye className="h-5 w-5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300" />
                    )}
                  </button>
                </div>
                {errors.password && (
                  <p className="mt-2 text-sm text-red-600 dark:text-red-400">
                    {errors.password}
                  </p>
                )}
                {formData.password && (
                  <div className="mt-2">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-xs text-gray-600 dark:text-gray-400">
                        Password strength:
                      </span>
                      <span
                        className={`text-xs font-medium ${
                          passwordStrength < 2
                            ? "text-red-600"
                            : passwordStrength < 3
                            ? "text-yellow-600"
                            : "text-green-600"
                        }`}
                      >
                        {getStrengthText(passwordStrength)}
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-1.5">
                      <div
                        className={`h-1.5 rounded-full ${getStrengthColor(
                          passwordStrength
                        )} transition-all duration-300`}
                        style={{ width: `${(passwordStrength / 4) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                )}
              </div>

              {/* Confirm Password Field */}
              <div>
                <label htmlFor="confirmPassword" className="sr-only">
                  Confirm password
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Lock className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="confirmPassword"
                    name="confirmPassword"
                    type={showConfirmPassword ? "text" : "password"}
                    autoComplete="new-password"
                    required
                    value={formData.confirmPassword}
                    onChange={handleInputChange}
                    className={`appearance-none relative block w-full pl-10 pr-10 py-3 border ${
                      errors.confirmPassword
                        ? "border-red-300 dark:border-red-600"
                        : "border-gray-300 dark:border-gray-600"
                    } placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white bg-white dark:bg-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 dark:focus:border-purple-400 transition-colors duration-200`}
                    placeholder="Confirm password"
                  />
                  <button
                    type="button"
                    className="absolute inset-y-0 right-0 pr-3 flex items-center"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  >
                    {showConfirmPassword ? (
                      <EyeOff className="h-5 w-5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300" />
                    ) : (
                      <Eye className="h-5 w-5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300" />
                    )}
                  </button>
                </div>
                {errors.confirmPassword && (
                  <p className="mt-2 text-sm text-red-600 dark:text-red-400">
                    {errors.confirmPassword}
                  </p>
                )}
              </div>

              {/* Terms and Privacy */}
              <div className="text-xs text-gray-600 dark:text-gray-400 text-center">
                By creating an account, you agree to our{" "}
                <Link
                  to="/terms"
                  className="text-purple-600 hover:text-purple-500 dark:text-purple-400"
                >
                  Terms of Service
                </Link>{" "}
                and{" "}
                <Link
                  to="/privacy"
                  className="text-purple-600 hover:text-purple-500 dark:text-purple-400"
                >
                  Privacy Policy
                </Link>
              </div>

              {/* Submit Button */}
              <div>
                <motion.button
                  type="submit"
                  disabled={isLoading}
                  className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                  whileHover={{ scale: isLoading ? 1 : 1.02 }}
                  whileTap={{ scale: isLoading ? 1 : 0.98 }}
                >
                  {isLoading ? (
                    <div className="flex items-center">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Creating account...
                    </div>
                  ) : (
                    <div className="flex items-center">
                      <UserPlus className="h-4 w-4 mr-2" />
                      Create account
                      <ArrowRight className="h-4 w-4 ml-2 group-hover:translate-x-1 transition-transform" />
                    </div>
                  )}
                </motion.button>
              </div>
            </form>

            {/* Sign In Link */}
            <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-600">
              <p className="text-center text-sm text-gray-600 dark:text-gray-400">
                Already have an account?{" "}
                <Link
                  to="/signin"
                  className="font-medium text-purple-600 hover:text-purple-500 dark:text-purple-400 dark:hover:text-purple-300"
                >
                  Sign in here
                </Link>
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default SignUpPage;
