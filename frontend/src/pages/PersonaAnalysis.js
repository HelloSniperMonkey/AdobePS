import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, Users, Target, FileText, Star, TrendingUp } from 'lucide-react';

const PersonaAnalysis = () => {
  const [pdfFiles, setPdfFiles] = useState([]);
  const [personaDescription, setPersonaDescription] = useState('');
  const [jobToBeDone, setJobToBeDone] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const onDrop = (acceptedFiles) => {
    const pdfFiles = acceptedFiles.filter(file => file.type === 'application/pdf');
    if (pdfFiles.length < 3) {
      setError('Please upload at least 3 PDF files for persona analysis.');
      return;
    }
    if (pdfFiles.length > 10) {
      setError('Please upload no more than 10 PDF files.');
      return;
    }
    
    setPdfFiles(pdfFiles);
    setError(null);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: true
  });

  const handleAnalysis = async () => {
    if (!personaDescription.trim() || !jobToBeDone.trim()) {
      setError('Please provide both persona description and job-to-be-done.');
      return;
    }

    if (pdfFiles.length < 3) {
      setError('Please upload at least 3 PDF files.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // For demo purposes, we'll simulate the API call
      // In production, you'd upload files and call the actual API
      const mockAnalysis = {
        metadata: {
          documents: pdfFiles.map(f => f.name),
          persona_description: personaDescription,
          job_to_be_done: jobToBeDone,
          timestamp: Date.now(),
          processing_time: 2.5
        },
        extracted_sections: [
          {
            document: pdfFiles[0]?.name || 'document1.pdf',
            page: 5,
            section_title: 'Introduction to Machine Learning',
            importance_rank: 0.95,
            similarity_score: 0.92,
            level: 'H1'
          },
          {
            document: pdfFiles[1]?.name || 'document2.pdf',
            page: 12,
            section_title: 'Neural Network Architectures',
            importance_rank: 0.88,
            similarity_score: 0.85,
            level: 'H2'
          },
          {
            document: pdfFiles[2]?.name || 'document3.pdf',
            page: 8,
            section_title: 'Deep Learning Applications',
            importance_rank: 0.82,
            similarity_score: 0.78,
            level: 'H1'
          }
        ],
        sub_section_analyses: [
          {
            document: pdfFiles[0]?.name || 'document1.pdf',
            refined_text: "This section on 'Introduction to Machine Learning' is highly relevant to your needs. It appears on page 5 and addresses key aspects related to your persona and objectives.",
            page: 5,
            original_title: 'Introduction to Machine Learning',
            relevance_explanation: "'Introduction to Machine Learning' directly addresses your primary objectives with high relevance."
          },
          {
            document: pdfFiles[1]?.name || 'document2.pdf',
            refined_text: "This section on 'Neural Network Architectures' is moderately relevant to your needs. It appears on page 12 and addresses key aspects related to your persona and objectives.",
            page: 12,
            original_title: 'Neural Network Architectures',
            relevance_explanation: "'Neural Network Architectures' provides valuable context and supporting information for your goals."
          }
        ]
      };

      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      setAnalysis(mockAnalysis);
    } catch (err) {
      setError('Error performing persona analysis: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const removeFile = (index) => {
    setPdfFiles(files => files.filter((_, i) => i !== index));
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Persona-Driven Analysis</h1>
        <p className="text-gray-600">
          Upload 3-10 related PDFs and provide your persona details to get personalized insights and recommendations.
        </p>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        {/* Input Section */}
        <div className="space-y-6">
          {/* PDF Upload */}
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <FileText className="w-5 h-5 mr-2" />
              Upload PDF Documents
            </h2>
            
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${
                isDragActive ? 'border-blue-400 bg-blue-50' : 'border-gray-300 hover:border-gray-400'
              }`}
            >
              <input {...getInputProps()} />
              <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
              <p className="text-sm text-gray-600">
                {isDragActive ? 'Drop PDFs here' : 'Drag & drop 3-10 PDF files here, or click to select'}
              </p>
              <p className="text-xs text-gray-500 mt-1">Minimum 3, maximum 10 files</p>
            </div>

            {pdfFiles.length > 0 && (
              <div className="mt-4 space-y-2">
                <h3 className="font-medium text-gray-900">Selected Files ({pdfFiles.length})</h3>
                {pdfFiles.map((file, index) => (
                  <div key={index} className="flex items-center justify-between bg-gray-50 p-2 rounded">
                    <span className="text-sm text-gray-700 truncate">{file.name}</span>
                    <button
                      onClick={() => removeFile(index)}
                      className="text-red-500 hover:text-red-700 text-sm"
                    >
                      Remove
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Persona Description */}
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <Users className="w-5 h-5 mr-2" />
              Persona Description
            </h2>
            <textarea
              value={personaDescription}
              onChange={(e) => setPersonaDescription(e.target.value)}
              placeholder="Describe your role, background, expertise level, and research interests..."
              className="w-full h-32 p-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Job to be Done */}
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <Target className="w-5 h-5 mr-2" />
              Job to be Done
            </h2>
            <textarea
              value={jobToBeDone}
              onChange={(e) => setJobToBeDone(e.target.value)}
              placeholder="What specific task or objective are you trying to accomplish with these documents?"
              className="w-full h-24 p-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Analysis Button */}
          <button
            onClick={handleAnalysis}
            disabled={loading || pdfFiles.length < 3 || !personaDescription.trim() || !jobToBeDone.trim()}
            className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
          >
            {loading ? (
              <>
                <div className="spinner w-5 h-5 mr-2"></div>
                Analyzing Documents...
              </>
            ) : (
              'Start Persona Analysis'
            )}
          </button>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-red-600 text-sm">{error}</p>
            </div>
          )}
        </div>

        {/* Results Section */}
        <div className="space-y-6">
          {analysis && (
            <>
              {/* Metadata */}
              <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Analysis Results</h2>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-gray-500">Processing Time:</span>
                    <div className="font-medium">{analysis.metadata.processing_time.toFixed(2)}s</div>
                  </div>
                  <div>
                    <span className="text-gray-500">Documents Analyzed:</span>
                    <div className="font-medium">{analysis.metadata.documents.length}</div>
                  </div>
                </div>
              </div>

              {/* Top Sections */}
              <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <Star className="w-5 h-5 mr-2" />
                  Top Recommended Sections
                </h3>
                <div className="space-y-3">
                  {analysis.extracted_sections.slice(0, 5).map((section, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-3">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-medium text-gray-900">{section.section_title}</h4>
                        <span className="text-sm text-gray-500">p.{section.page}</span>
                      </div>
                      <div className="flex items-center space-x-4 text-sm text-gray-600">
                        <span>Rank: {(section.importance_rank * 100).toFixed(0)}%</span>
                        <span>Similarity: {(section.similarity_score * 100).toFixed(0)}%</span>
                        <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                          {section.level}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Detailed Analyses */}
              <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <TrendingUp className="w-5 h-5 mr-2" />
                  Detailed Insights
                </h3>
                <div className="space-y-4">
                  {analysis.sub_section_analyses.map((analysis, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4">
                      <h4 className="font-medium text-gray-900 mb-2">{analysis.original_title}</h4>
                      <p className="text-sm text-gray-600 mb-2">{analysis.refined_text}</p>
                      <p className="text-xs text-gray-500">{analysis.relevance_explanation}</p>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}

          {!analysis && !loading && (
            <div className="bg-gray-50 rounded-lg p-8 text-center">
              <Users className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                Ready for Analysis
              </h3>
              <p className="text-gray-600">
                Upload your PDFs and provide persona details to get personalized insights and recommendations.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PersonaAnalysis; 