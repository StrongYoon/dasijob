export class JobWebSocket {
  constructor(userId) {
    this.socket = new WebSocket(
      `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/ws/jobs/updates/`
    );
    this.handlers = new Map();

    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const handler = this.handlers.get(data.type);
      if (handler) {
        handler(data.data);
      }
    };

    this.socket.onclose = () => {
      console.log('WebSocket disconnected. Attempting to reconnect...');
      setTimeout(() => {
        this.constructor(userId);
      }, 5000);
    };
  }

  addHandler(type, callback) {
    this.handlers.set(type, callback);
  }

  removeHandler(type) {
    this.handlers.delete(type);
  }
}

// 대시보드에서 사용 예시:
import {JobWebSocket} from './websocket';

const Dashboard = () => {
  useEffect(() => {
    const socket = new JobWebSocket(userId);

    socket.addHandler('job_update', (data) => {
      // 채용 정보 업데이트 처리
      console.log('Job update received:', data);
    });

    socket.addHandler('application_update', (data) => {
      // 지원 현황 업데이트 처리
      console.log('Application update received:', data);
    });

    return () => {
      socket.socket.close();
    };
  }, []);

  // ... 나머지 대시보드 컴포넌트 코드
};