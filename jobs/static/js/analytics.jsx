import React, {useEffect, useState} from 'react';
import {Card, CardContent} from '@/components/ui/card';
import {
  Bar,
  BarChart,
  Cell,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from 'recharts';

const AnalyticsDashboard = () => {
  const [analytics, setAnalytics] = useState({
    jobTrends: [],
    categoryStats: [],
    locationStats: [],
    salaryStats: {}
  });

  useEffect(() => {
    // 실제 구현시 API 호출로 대체
    setAnalytics({
      jobTrends: [
        { month: '1월', count: 45 },
        { month: '2월', count: 52 },
        { month: '3월', count: 48 }
      ],
      categoryStats: [
        { name: 'IT', value: 35 },
        { name: '경영', value: 25 },
        { name: '디자인', value: 20 },
        { name: '마케팅', value: 20 }
      ],
      locationStats: [
        { location: '서울', count: 150 },
        { location: '경기', count: 80 },
        { location: '부산', count: 40 },
        { location: '기타', count: 30 }
      ],
      salaryStats: {
        average: 4500,
        min: 3000,
        max: 7000
      }
    });
  }, []);

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  return (
    <div className="p-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardContent className="p-6">
            <h3 className="text-lg font-semibold mb-4">채용공고 추이</h3>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={analytics.jobTrends}>
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="count" stroke="#3b82f6" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <h3 className="text-lg font-semibold mb-4">직무별 분포</h3>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={analytics.categoryStats}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    dataKey="value"
                    label
                  >
                    {analytics.categoryStats.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <h3 className="text-lg font-semibold mb-4">지역별 채용 현황</h3>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={analytics.locationStats}>
                  <XAxis dataKey="location" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="count" fill="#3b82f6" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <h3 className="text-lg font-semibold mb-4">급여 통계</h3>
            <div className="space-y-4">
              <div>
                <p className="text-gray-500">평균 급여</p>
                <p className="text-2xl font-semibold">{analytics.salaryStats.average}만원</p>
              </div>
              <div>
                <p className="text-gray-500">최저 - 최고 급여</p>
                <p className="text-lg">
                  {analytics.salaryStats.min}만원 - {analytics.salaryStats.max}만원
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;