import React from "react";
import { motion } from "framer-motion";
import { Brain } from "lucide-react";

interface LoadingSpinnerProps {
  size?: "sm" | "md" | "lg";
  message?: string;
  fullScreen?: boolean;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = "md",
  message = "Loading...",
  fullScreen = true,
}) => {
  const sizeClasses = {
    sm: "w-6 h-6",
    md: "w-8 h-8",
    lg: "w-12 h-12",
  };

  const textSizeClasses = {
    sm: "text-sm",
    md: "text-base",
    lg: "text-lg",
  };

  const spinnerContent = (
    <div className="flex flex-col items-center justify-center space-y-4">
      <motion.div
        animate={{ rotate: 360 }}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: "linear",
        }}
        className="relative"
      >
        <div
          className={`${sizeClasses[size]} bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center`}
        >
          <Brain
            className={`${
              size === "sm" ? "w-3 h-3" : size === "md" ? "w-4 h-4" : "w-6 h-6"
            } text-white`}
          />
        </div>
        <motion.div
          animate={{ rotate: -360 }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
            ease: "linear",
          }}
          className={`absolute -inset-2 border-2 border-transparent border-t-blue-500 border-r-purple-500 rounded-full`}
        />
      </motion.div>

      {message && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className={`${textSizeClasses[size]} text-gray-600 dark:text-gray-400 font-medium`}
        >
          {message}
        </motion.p>
      )}
    </div>
  );

  if (fullScreen) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        {spinnerContent}
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center p-8">{spinnerContent}</div>
  );
};

export default LoadingSpinner;
