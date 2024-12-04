import React, {useEffect, useState} from 'react';
import {Card, CardContent} from '@/components/ui/card';
import {Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis} from 'recharts';
import {Bell, Briefcase, FileText, Users} from 'lucide-react';

const Dashboard = () => {
  const [stats, setStats] = useState({
    applications: 0,
    inProgress: 0,
    completedResumes: 0,
    notifications: 0
  });

  const [applicationTrend, setApplicationTrend] = useState([]);

  useEffect(() => {
    // 실제 구현시 API 호출로 대체
    setStats({
      applications: 12,
      inProgress: 4,
      completedResumes: 3,
      notifications: 7
    });

    setApplicationTrend([
      { date: '2024-01', count: 5 },
      { date: '2024-02', count: 8 },
      { date: '2024-03', count: 12 }
    ]);
  }, []);

  const statCards = [
    { title: '총 지원', value: stats.applications, icon: <Briefcase className="w-6 h-6" /> },
    { title: '진행중', value: stats.inProgress, icon: <Users className="w-6 h-6" /> },
    { title: '완료된 이력서', value: stats.completedResumes, icon: <FileText className="w-6 h-6" /> },
    { title: '새로운 알림', value: stats.notifications, icon: <Bell className="w-6 h-6" /> }
  ];

  return (
    <div className="p-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {statCards.map((stat, index) => (
          <Card key={index}>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-500 text-sm">{stat.title}</p>
                  <p className="text-2xl font-semibold mt-1">{stat.value}</p>
                </div>
                <div className="text-blue-500">{stat.icon}</div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card className="mb-8">
        <CardContent className="p-6">
          <h3 className="text-lg font-semibold mb-4">지원 현황 추이</h3>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={applicationTrend}>
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="count" stroke="#3b82f6" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Dashboard;