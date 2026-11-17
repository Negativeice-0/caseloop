/* ----------------------------------------------------
   Copyright (c) 2026 Billy Gates Ochieng Osodo. All Rights Reserved.
   CaseLoop Humanitarian Coordination System - Response Register Module
   ---------------------------------------------------- */

import React, { useEffect, useState } from 'react';
import { fetchResponses, createResponse, deleteResponse, updateResponse } from '../../services/api';
import { ResponseItem } from '../../types';
import { PlusCircle, Search, Trash2, AlertCircle, Pencil } from 'lucide-react';

interface ResponseRegisterProps {
  userRole: 'admin' | 'coordinator' | 'responder';
  mode?: 'read-only' | 'admin';
}

export default function ResponseRegister({ userRole, mode = 'read-only' }: ResponseRegisterProps) {
  const canManage = mode === 'admin' && userRole !== 'responder';
  const canDelete = mode === 'admin' && userRole === 'admin';
  const [responses, setResponses] = useState<ResponseItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');

  const [showForm, setShowForm] = useState(false);
  const [refCode, setRefCode] = useState('');
  const [editingResponse, setEditingResponse] = useState<ResponseItem | null>(null);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [category, setCategory] = useState('Community assistance');
  const [priority, setPriority] = useState('normal');
  const [location, setLocation] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const loadResponses = async () => {
    try {
      setLoading(true);
      const data = await fetchResponses();
      setResponses(data);
      setError(null);
    } catch (err: any) {
      setError('Failed to fetch response records from the configured database.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadResponses();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setSubmitting(true);
      const payload = {
        reference_code: refCode,
        title,
        description,
        category,
        priority,
        location,
      };
      if (editingResponse) {
        await updateResponse(editingResponse.id, payload);
      } else {
        await createResponse(payload);
      }
      setTitle('');
      setDescription('');
      setRefCode('');
      setLocation('');
      setEditingResponse(null);
      setShowForm(false);
      await loadResponses();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to save response.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleEdit = (item: ResponseItem) => {
    setEditingResponse(item);
    setRefCode(item.reference_code);
    setTitle(item.title);
    setDescription(item.description || '');
    setCategory(item.category || 'Community assistance');
    setPriority(item.priority || 'normal');
    setLocation(item.location || '');
    setShowForm(true);
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to remove this operational response record?')) return;
    try {
      await deleteResponse(id);
      await loadResponses();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to delete response.');
    }
  };

  const filteredResponses = responses.filter(r => 
    r.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    r.reference_code.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (r.category || '').toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Action Header */}
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-3 bg-white border border-slate-200 px-4 py-2.5 rounded-2xl shadow-sm flex-1 max-w-md">
          <Search className="w-4 h-4 text-slate-400" />
          <input 
            type="text" 
            placeholder="Search active responses..." 
            value={searchTerm} 
            onChange={(e) => setSearchTerm(e.target.value)} 
            className="w-full bg-transparent text-sm focus:outline-none" 
          />
        </div>
        {canManage && (
          <button
            onClick={() => {
              if (showForm) {
                setEditingResponse(null);
                setRefCode('');
                setTitle('');
                setDescription('');
                setLocation('');
              }
              setShowForm(!showForm);
            }}
            className="inline-flex items-center justify-center gap-2 bg-red-600 hover:bg-red-700 text-white font-bold px-5 py-2.5 rounded-xl shadow-lg shadow-red-600/30 text-sm transition"
          >
            <PlusCircle className="w-4 h-4" /> New Response
          </button>
        )}
      </div>

      {error && (
        <div className="p-4 rounded-2xl bg-amber-50 border border-amber-200 text-amber-800 flex items-center gap-3 text-sm shadow-sm">
          <AlertCircle className="w-5 h-5 flex-shrink-0 text-amber-600" />
          <span className="font-medium">{error}</span>
        </div>
      )}

      {/* Creation Form Modal/Panel */}
      {showForm && (
        <div className="bg-white border border-slate-200 p-6 rounded-2xl shadow-xl">
          <h3 className="text-base font-black mb-4 text-slate-900">{editingResponse ? 'Update response record' : 'Create New Operational Response Record'}</h3>
          <form onSubmit={handleCreate} className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1 uppercase">Reference Code</label>
              <input type="text" required value={refCode} onChange={(e) => setRefCode(e.target.value)} className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2 text-sm font-mono" />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1 uppercase">Location</label>
              <input type="text" value={location} onChange={(e) => setLocation(e.target.value)} className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2 text-sm" />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1 uppercase">Response Title</label>
              <input type="text" required placeholder="e.g., Karen Medical Camp" value={title} onChange={(e) => setTitle(e.target.value)} className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2 text-sm" />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1 uppercase">Category</label>
              <select value={category} onChange={(e) => setCategory(e.target.value)} className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2 text-sm">
                <option value="Community assistance">Community assistance</option>
                <option value="Disaster response">Disaster response</option>
                <option value="Emergency support">Emergency support</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1 uppercase">Priority</label>
              <select value={priority} onChange={(e) => setPriority(e.target.value)} className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2 text-sm">
                <option value="normal">Normal</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>
            <div className="md:col-span-2">
              <label className="block text-xs font-bold text-slate-700 mb-1 uppercase">Description</label>
              <textarea rows={2} value={description} onChange={(e) => setDescription(e.target.value)} className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2 text-sm"></textarea>
            </div>
            <div className="md:col-span-2 flex justify-end gap-3">
              <button type="button" onClick={() => { setShowForm(false); setEditingResponse(null); }} className="px-4 py-2 rounded-xl bg-slate-200 text-sm font-bold text-slate-700">Cancel</button>
              <button type="submit" disabled={submitting} className="px-5 py-2 rounded-xl bg-red-600 text-white text-sm font-bold shadow-md">{editingResponse ? 'Save changes' : 'Save Record'}</button>
            </div>
          </form>
        </div>
      )}

      {/* Response Data Table */}
      <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-xl">
        <div className="px-6 py-4 border-b border-slate-200 flex justify-between bg-slate-50">
          <h3 className="font-black text-sm text-slate-800 uppercase">Operational Records ({filteredResponses.length})</h3>
          <span className="text-xs font-bold text-red-600 bg-red-50 border border-red-200 px-2 py-0.5 rounded font-mono">Operational data</span>
        </div>
        {loading ? (
          <div className="p-12 text-center text-sm text-slate-500 animate-pulse">Loading local records...</div>
        ) : filteredResponses.length === 0 ? (
          <div className="p-12 text-center text-sm text-slate-500">No response records found.</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-100 text-xs uppercase font-bold text-slate-600">
                <tr>
                  <th className="px-6 py-3">Reference</th>
                  <th className="px-6 py-3">Title</th>
                  <th className="px-6 py-3">Category</th>
                  <th className="px-6 py-3">Priority</th>
                  <th className="px-6 py-3">Status</th>
                  {canManage && <th className="px-6 py-3 text-right">Actions</th>}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200">
                {filteredResponses.map((item) => (
                  <tr key={item.id} className="hover:bg-red-50/40 transition">
                    <td className="px-6 py-4 font-mono text-xs font-black text-red-600">{item.reference_code}</td>
                    <td className="px-6 py-4 font-bold text-slate-900">{item.title}</td>
                    <td className="px-6 py-4 text-slate-600 text-xs">{item.category}</td>
                    <td className="px-6 py-4 uppercase text-xs font-bold">{item.priority}</td>
                    <td className="px-6 py-4 text-emerald-700 text-xs font-bold">{item.status}</td>
                    {canManage && <td className="px-6 py-4 text-right">
                      <div className="flex justify-end gap-2">
                        {canManage && <button onClick={() => handleEdit(item)} className="p-1.5 text-slate-400 hover:text-slate-900 rounded-lg" title="Edit response"><Pencil className="w-4 h-4" /></button>}
                        {canDelete && <button onClick={() => handleDelete(item.id)} className="p-1.5 text-slate-400 hover:text-red-600 rounded-lg transition" title="Delete Record"><Trash2 className="w-4 h-4" /></button>}
                      </div>
                    </td>}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}