const { MapPin, Search } = window.lucide;

const LocationSearch = function() {
  // useState -> React.useState로 변경
  const [sido, setSido] = React.useState('');
  const [sigungu, setSigungu] = React.useState('');
  const [dong, setDong] = React.useState('');
  const [keyword, setKeyword] = React.useState('');
  const [locations, setLocations] = React.useState({ sido: [], sigungu: [], dong: [] });
  const [isLoading, setIsLoading] = React.useState(false);

  // API 호출 함수
  const fetchRegions = async (level, parentCode = null) => {
    setIsLoading(true);
    try {
      const params = new URLSearchParams({ level });
      if (parentCode) params.append('parent_code', parentCode);

      const response = await fetch(`/api/regions/?${params}`);
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching regions:', error);
      return [];
    } finally {
      setIsLoading(false);
    }
  };

   // useEffect도 React.useEffect로 변경
  React.useEffect(() => {
    const loadSido = async () => {
      const sidoData = await fetchRegions('1');
      setLocations(prev => ({ ...prev, sido: sidoData }));
    };
    loadSido();
  }, []);

  React.useEffect(() => {
    const loadSigungu = async () => {
      if (sido) {
        const sigunguData = await fetchRegions('2', sido);
        setLocations(prev => ({ ...prev, sigungu: sigunguData }));
        setSigungu('');
        setDong('');
      }
    };
    loadSigungu();
  }, [sido]);

  React.useEffect(() => {
    const loadDong = async () => {
      if (sigungu) {
        const dongData = await fetchRegions('3', sigungu);
        setLocations(prev => ({ ...prev, dong: dongData }));
        setDong('');
      }
    };
    loadDong();
  }, [sigungu]);

  const handleSearch = (e) => {
    e.preventDefault();
    // 검색 로직 구현
    const searchParams = new URLSearchParams({
      sido: sido || '',
      sigungu: sigungu || '',
      dong: dong || '',
      keyword: keyword || ''
    });
    window.location.href = `/jobs/search/?${searchParams}`;
  };

  return (
    <form onSubmit={handleSearch} className="bg-white rounded-lg shadow-lg p-4 md:p-6">
      <div className="flex flex-col space-y-4">
        <div className="flex items-center space-x-2 text-lg font-semibold text-gray-700">
          <MapPin className="w-5 h-5 text-blue-500" />
          <span>근처 일자리 찾기</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* 시/도 선택 */}
          <div className="relative">
            <select
              value={sido}
              onChange={(e) => setSido(e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-lg"
              disabled={isLoading}
            >
              <option value="">시/도 선택</option>
              {locations.sido.map((item) => (
                <option key={item.code} value={item.code}>{item.name}</option>
              ))}
            </select>
          </div>

          {/* 시/군/구 선택 */}
          <div className="relative">
            <select
              value={sigungu}
              onChange={(e) => setSigungu(e.target.value)}
              disabled={!sido || isLoading}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-lg"
            >
              <option value="">시/군/구 선택</option>
              {locations.sigungu.map((item) => (
                <option key={item.code} value={item.code}>{item.name}</option>
              ))}
            </select>
          </div>

          {/* 동/읍/면 선택 */}
          <div className="relative">
            <select
              value={dong}
              onChange={(e) => setDong(e.target.value)}
              disabled={!sigungu || isLoading}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-lg"
            >
              <option value="">동/읍/면 선택</option>
              {locations.dong.map((item) => (
                <option key={item.code} value={item.code}>{item.name}</option>
              ))}
            </select>
          </div>
        </div>

        {/* 검색어 입력 및 검색 버튼 */}
        <div className="flex space-x-4">
          <div className="flex-1">
            <div className="relative">
              <input
                type="text"
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
                placeholder="찾으시는 일자리를 입력해주세요 (예: 경비원, 주차관리)"
                className="w-full p-3 pl-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-lg"
              />
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            </div>
          </div>
          <button
            type="submit"
            className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:ring-4 focus:ring-blue-300 text-lg font-semibold"
            disabled={isLoading}
          >
            검색
          </button>
        </div>

        {/* 인기 검색어 */}
        <div className="flex flex-wrap gap-2 mt-2">
          <span className="text-sm text-gray-500">인기 검색어:</span>
          {['경비원', '주차관리', '식당도우미', '판매직', '사무보조'].map((term) => (
            <button
              key={term}
              type="button"
              onClick={() => setKeyword(term)}
              className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200"
            >
              {term}
            </button>
          ))}
        </div>
      </div>
    </form>
  );
};


window.LocationSearch = LocationSearch;