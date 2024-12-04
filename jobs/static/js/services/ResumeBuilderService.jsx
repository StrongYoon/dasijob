import React, {useEffect, useState} from 'react';
import {Alert, AlertDescription} from '@/components/ui/alert';

const ResumeBuilderService = () => {
  const [resume, setResume] = useState(null);
  const [error, setError] = useState(null);
  const [saveStatus, setSaveStatus] = useState('idle');

  const loadResume = async (id) => {
    try {
      const response = await fetch(`/api/resumes/${id}/`);
      if (!response.ok) throw new Error('이력서를 불러올 수 없습니다.');
      const data = await response.json();
      setResume(data);
    } catch (err) {
      setError(err.message);
    }
  };

  const saveResume = async (content, isDraft = true) => {
    setSaveStatus('saving');
    try {
      const endpoint = isDraft ? 'save_draft' : 'publish';
      const response = await fetch(`/api/resumes/${resume.id}/${endpoint}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: JSON.stringify({ content }),
      });

      if (!response.ok) throw new Error('저장에 실패했습니다.');

      setSaveStatus('saved');
      setTimeout(() => setSaveStatus('idle'), 2000);
    } catch (err) {
      setError(err.message);
      setSaveStatus('error');
    }
  };

  // 자동 저장 기능
  useEffect(() => {
    let autoSaveTimer;
    if (resume?.content_json) {
      autoSaveTimer = setTimeout(() => {
        saveResume(resume.content_json, true);
      }, 30000); // 30초마다 자동 저장
    }
    return () => clearTimeout(autoSaveTimer);
  }, [resume?.content_json]);

  return (
    <div className="space-y-4">
      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {saveStatus === 'saving' && (
        <Alert>
          <AlertDescription>저장 중...</AlertDescription>
        </Alert>
      )}

      {saveStatus === 'saved' && (
        <Alert>
          <AlertDescription>저장되었습니다!</AlertDescription>
        </Alert>
      )}

      <div className="flex justify-end space-x-4">
        <button
          onClick={() => saveResume(resume.content_json, true)}
          className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
        >
          임시저장
        </button>
        <button
          onClick={() => saveResume(resume.content_json, false)}
          className="px-4 py-2 text-white bg-blue-500 rounded-lg hover:bg-blue-600"
        >
          발행하기
        </button>
      </div>
    </div>
  );
};

export default ResumeBuilderService;