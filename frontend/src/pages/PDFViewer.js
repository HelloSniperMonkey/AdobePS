import React, { useState, useRef, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, ChevronDown, ChevronRight, Eye } from 'lucide-react';
import axios from 'axios';

const PDFViewer = () => {
  const [pdfFile, setPdfFile] = useState(null);
  const [pdfUrl, setPdfUrl] = useState(null);
  const [outline, setOutline] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [expandedSections, setExpandedSections] = useState(new Set());
  const adobeViewerRef = useRef(null);

  // Adobe PDF Embed API configuration
  const adobeConfig = {
    clientId: "YOUR_ADOBE_CLIENT_ID", // Replace with actual client ID
    divId: "adobe-dc-view",
  };

  // Initialize Adobe PDF Embed API
  useEffect(() => {
    if (pdfUrl && window.AdobeDC) {
      const viewer = window.AdobeDC.View.createViewer(adobeViewerRef.current, adobeConfig);
      viewer.previewFile({
        content: { location: { url: pdfUrl } },
        metaData: { fileName: pdfFile?.name || "document.pdf" }
      });
    }
  }, [pdfUrl]);

  const onDrop = async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file && file.type === 'application/pdf') {
      setPdfFile(file);
      setError(null);
      
      // Create URL for PDF viewer
      const url = URL.createObjectURL(file);
      setPdfUrl(url);
      
      // Extract outline
      await extractOutline(file);
    } else {
      setError('Please upload a valid PDF file.');
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: false
  });

  const extractOutline = async (file) => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post('/extract-outline', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.success) {
        setOutline(response.data.result);
      } else {
        setError('Failed to extract outline from PDF.');
      }
    } catch (err) {
      setError('Error processing PDF: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const toggleSection = (index) => {
    const newExpanded = new Set(expandedSections);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedSections(newExpanded);
  };

  const navigateToPage = (pageNumber) => {
    if (adobeViewerRef.current) {
      // Adobe PDF Embed API navigation
      adobeViewerRef.current.getAPIs().then((apis) => {
        apis.getPageViewAPI().then((pageViewAPI) => {
          pageViewAPI.goToPage(pageNumber);
        });
      });
    }
  };



  const renderOutlineItem = (item, index, level = 0) => {
    const isExpanded = expandedSections.has(index);
    const hasChildren = item.children && item.children.length > 0;

    return (
      <div key={index} className="outline-item-container">
        <div
          className={`outline-item ${item.level.toLowerCase()}`}
          style={{ paddingLeft: `${16 + level * 16}px` }}
          onClick={() => navigateToPage(item.page)}
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              {hasChildren && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    toggleSection(index);
                  }}
                  className="p-1 hover:bg-gray-200 rounded"
                >
                  {isExpanded ? (
                    <ChevronDown className="w-3 h-3" />
                  ) : (
                    <ChevronRight className="w-3 h-3" />
                  )}
                </button>
              )}
              <FileText className="w-4 h-4 text-gray-400" />
              <span className="truncate">{item.text}</span>
            </div>
            <span className="text-xs text-gray-500">p.{item.page}</span>
          </div>
        </div>
        
        {hasChildren && isExpanded && (
          <div className="ml-4">
            {item.children.map((child, childIndex) =>
              renderOutlineItem(child, `${index}-${childIndex}`, level + 1)
            )}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <div className="sidebar">
        <div className="p-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Document Outline</h2>
          
          {!pdfFile && (
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${
                isDragActive ? 'border-blue-400 bg-blue-50' : 'border-gray-300 hover:border-gray-400'
              }`}
            >
              <input {...getInputProps()} />
              <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
              <p className="text-sm text-gray-600">
                {isDragActive ? 'Drop the PDF here' : 'Drag & drop a PDF file here, or click to select'}
              </p>
            </div>
          )}

          {loading && (
            <div className="flex items-center justify-center py-8">
              <div className="spinner"></div>
              <span className="ml-2 text-gray-600">Extracting outline...</span>
            </div>
          )}

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-3 mb-4">
              <p className="text-red-600 text-sm">{error}</p>
            </div>
          )}

          {outline && (
            <div>
              <h3 className="font-medium text-gray-900 mb-2">{outline.title}</h3>
              <div className="space-y-1">
                {outline.outline.map((item, index) => renderOutlineItem(item, index))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* PDF Viewer */}
      <div className="flex-1 flex flex-col">
        {pdfUrl ? (
          <div className="flex-1">
            <div
              ref={adobeViewerRef}
              id="adobe-dc-view"
              className="pdf-container"
            ></div>
          </div>
        ) : (
          <div className="flex-1 flex items-center justify-center bg-gray-50">
            <div className="text-center">
              <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                No PDF Selected
              </h3>
              <p className="text-gray-600 mb-4">
                Upload a PDF file to start analyzing its structure
              </p>
              <button
                onClick={() => document.querySelector('input[type="file"]').click()}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Choose PDF File
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PDFViewer; 