import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

const ProjectList = ({ onProjectSelect }) => {
    const [projects, setProjects] = useState([]);
    const [users, setUsers] = useState([]);
    const [error, setError] = useState('');
    const [sortBy, setSortBy] = useState('created');
    const [currentUserId, setCurrentUserId] = useState(null);
    const [isSuperuser, setIsSuperuser] = useState(false);
    const [editingProjectId, setEditingProjectId] = useState(null);
    const [editedProject, setEditedProject] = useState({
        title: '',
        description: '',
        status: 'AC',
        project_users: [],
    });

    useEffect(() => {
        const fetchProjects = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/api/v1/projects/', {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    },
                    params: {
                        ordering: sortBy,
                    }
                });
                setProjects(response.data);
            } catch (error) {
                setError('Ошибка при загрузке проектов');
            }
        };

        const fetchUsers = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/api/v1/users/', {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    }
                });
                setUsers(response.data);
            } catch (error) {
                setError('Ошибка при загрузке пользователей');
            }
        };

        const token = localStorage.getItem('access_token');
        if (token) {
            const decodedToken = jwtDecode(token);
            setCurrentUserId(decodedToken.user_id);
            setIsSuperuser(decodedToken.is_superuser);
        }

        fetchProjects();
        fetchUsers();
    }, [sortBy]);

    const handleSortChange = (e) => {
        setSortBy(e.target.value);
    };

    const filterProjectsByUser = () => {
        if (isSuperuser) {
            return projects;
        } else if (currentUserId) {
            return projects.filter(project => project.project_users.includes(currentUserId) && project.status === 'AC');
        }
        return [];
    };

    const filteredProjects = filterProjectsByUser();

    const handleEditProject = (projectId) => {
        if (!isSuperuser) return;

        const projectToEdit = projects.find(project => project.id === projectId);
        if (projectToEdit) {
            setEditedProject({
                title: projectToEdit.title,
                description: projectToEdit.description,
                status: projectToEdit.status,
                project_users: projectToEdit.project_users,
            });
            setEditingProjectId(projectId);
        }
    };

    const handleSaveProject = async () => {
        if (!isSuperuser) return;

        try {
            await axios.put(`http://127.0.0.1:8000/api/v1/projects/${editingProjectId}/`, editedProject, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });
            const updatedProjects = projects.map(project => project.id === editingProjectId ? { ...project, ...editedProject } : project);
            setProjects(updatedProjects);
            setEditingProjectId(null);
        } catch (error) {
            setError('Ошибка при сохранении проекта');
        }
    };

    const handleCancelEdit = () => {
        setEditingProjectId(null);
    };

    const handleUserChange = (e) => {
        const options = e.target.options;
        const value = [];
        for (let i = 0, l = options.length; i < l; i++) {
            if (options[i].selected) {
                value.push(options[i].value);
            }
        }
        setEditedProject({ ...editedProject, project_users: value });
    };

    return (
        <div className="project-list-container">
            <div className="sort-controls">
                <label className='label_sort' htmlFor="sortBy">Сортировать по:</label>
                <select  className='sort_by' id="sortBy" value={sortBy} onChange={handleSortChange}>
                    <option value="created">Времени создания (от старых к новым)</option>
                    <option value="-created">Времени создания (от новых к старым)</option>
                    <option value="update">Времени обновления (от старых к новым)</option>
                    <option value="-update">Времени обновления (от новых к старым)</option>
                    <option value="title">Названию (от А до Я)</option>
                    <option value="-title">Названию (от Я до А)</option>
                </select>
            </div>
            {error && <div className="error-message">{error}</div>}
            {editingProjectId ? (
                <div className="edit-project-form">
                    <h3>Редактирование проекта</h3>
                    <div>
                        <label htmlFor="title">Название проекта:</label>
                        <input
                            type="text"
                            id="title"
                            value={editedProject.title}
                            onChange={(e) => setEditedProject({ ...editedProject, title: e.target.value })}
                        />
                    </div>
                    <div>
                        <label htmlFor="description">Описание:</label>
                        <textarea
                            id="description"
                            value={editedProject.description}
                            onChange={(e) => setEditedProject({ ...editedProject, description: e.target.value })}
                        />
                    </div>
                    <div>
                        <label htmlFor="status">Статус:</label>
                        <select
                            id="status"
                            value={editedProject.status}
                            onChange={(e) => setEditedProject({ ...editedProject, status: e.target.value })}
                        >
                            <option value="AC">Active</option>
                            <option value="AR">Archive</option>
                        </select>
                    </div>
                    <div>
                        <label htmlFor="project_users">Пользователи проекта:</label>
                        <select
                            id="project_users"
                            multiple
                            value={editedProject.project_users}
                            onChange={handleUserChange}
                        >
                            {users.map(user => (
                                <option key={user.id} value={user.id}>{user.username}</option>
                            ))}
                        </select>
                    </div>
                    <button type='submit' className='button' onClick={handleSaveProject}>Сохранить</button>
                    <button type='submit' className='button' onClick={handleCancelEdit}>Отмена</button>
                </div>
            ) : (
                <ul className="project-list">
                    {filteredProjects.map(project => (
                        <li key={project.id} className="project-item">
                            {isSuperuser && (
                                <div className="buttons_wrap">
                                    <button className="edit-button button" onClick={() => handleEditProject(project.id)}>Редактировать</button>
                                </div>
                            )}
                            <div onClick={() => onProjectSelect(project.id)}>
                                <h3>{project.title}</h3>
                                <p>{project.description}</p>
                                <p>Статус: {project.status === 'AC' ? 'Active' : 'Archive'}</p>
                                <p>Создан: {new Date(project.created).toLocaleString()}</p>
                                <p>Обновлен: {new Date(project.update).toLocaleString()}</p>
                            </div>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default ProjectList;