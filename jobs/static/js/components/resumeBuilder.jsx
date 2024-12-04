import React, {useState} from 'react';
import {DragDropContext, Draggable, Droppable} from 'react-beautiful-dnd';

const ResumeBuilder = () => {
  const [sections, setSections] = useState([
    { id: 'education', title: '학력', items: [] },
    { id: 'experience', title: '경력', items: [] },
    { id: 'skills', title: '기술스택', items: [] }
  ]);

  const onDragEnd = (result) => {
    if (!result.destination) return;

    const { source, destination } = result;
    const newSections = [...sections];
    const sourceSection = newSections.find(s => s.id === source.droppableId);
    const destSection = newSections.find(s => s.id === destination.droppableId);

    const [removed] = sourceSection.items.splice(source.index, 1);
    destSection.items.splice(destination.index, 0, removed);

    setSections(newSections);
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">이력서 빌더</h1>

      <DragDropContext onDragEnd={onDragEnd}>
        {sections.map(section => (
          <div key={section.id} className="mb-6">
            <h2 className="text-xl font-semibold mb-3">{section.title}</h2>
            <Droppable droppableId={section.id}>
              {(provided) => (
                <div
                  ref={provided.innerRef}
                  {...provided.droppableProps}
                  className="min-h-[100px] p-4 border-2 border-dashed border-gray-300 rounded-lg"
                >
                  {section.items.map((item, index) => (
                    <Draggable key={item.id} draggableId={item.id} index={index}>
                      {(provided) => (
                        <div
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          {...provided.dragHandleProps}
                          className="p-3 mb-2 bg-white shadow rounded-lg"
                        >
                          {item.content}
                        </div>
                      )}
                    </Draggable>
                  ))}
                  {provided.placeholder}
                </div>
              )}
            </Droppable>
          </div>
        ))}
      </DragDropContext>
    </div>
  );
};

export default ResumeBuilder;