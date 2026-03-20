/**
 * BotConfigForm.tsx
 * User interface for configuring trading bot
 */

import React, { useState, useEffect } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';

interface BotConfig {
  name: string;
  creators: string[];
  symbols: Record<string, number>;
  entryStagger: Record<string, number>;
  takeProfit: number;
  stopLoss: number;
  batchSize: number;
  waveInterval: number;
}

interface CreatorOption {
  id: string;
  name: string;
  tier: number;
  confidence: number;
  successRate: number;
}

export const BotConfigForm: React.FC = () => {
  const [config, setConfig] = useState<BotConfig>({
    name: 'My Trading Bot',
    creators: ['ForexMentor'],
    symbols: { ETHE: 0.5, GBTC: 0.4 },
    entryStagger: { ETHE: -0.02, GBTC: -0.01 },
    takeProfit: 0.03,
    stopLoss: -0.01,
    batchSize: 100,
    waveInterval: 90
  });

  // Fetch available creators from Research Agent
  const { data: creators, isLoading: creatorsLoading } = useQuery({
    queryKey: ['creators'],
    queryFn: async () => {
      const res = await fetch('/api/research/creators-library');
      return res.json() as Promise<CreatorOption[]>;
    }
  });

  // Mutation to generate orders
  const generateOrders = useMutation({
    mutationFn: async (cfg: BotConfig) => {
      const res = await fetch('/api/agent/generate-orders', {
        method: 'POST',
        body: JSON.stringify(cfg),
        headers: { 'Content-Type': 'application/json' }
      });
      return res.json();
    }
  });

  const handleCreatorToggle = (creatorId: string) => {
    setConfig(prev => ({
      ...prev,
      creators: prev.creators.includes(creatorId)
        ? prev.creators.filter(c => c !== creatorId)
        : [...prev.creators, creatorId]
    }));
  };

  const handleSymbolAllocation = (symbol: string, allocation: number) => {
    // Normalize allocations to sum to 100%
    const newSymbols = { ...config.symbols, [symbol]: allocation / 100 };
    const total = Object.values(newSymbols).reduce((a, b) => a + b, 0);
    
    // Normalize if over 100%
    if (total > 1) {
      Object.keys(newSymbols).forEach(sym => {
        newSymbols[sym] = newSymbols[sym] / total;
      });
    }
    
    setConfig(prev => ({
      ...prev,
      symbols: newSymbols
    }));
  };

  return (
    <div className="bot-config-form">
      <h2>Configure Your Trading Bot</h2>

      {/* Bot Name */}
      <div className="form-section">
        <label>Bot Name</label>
        <input
          type="text"
          value={config.name}
          onChange={(e) => setConfig({ ...config, name: e.target.value })}
          placeholder="e.g., ForexMentor Scalper"
        />
      </div>

      {/* Creator Selection */}
      <div className="form-section">
        <label>Select Creators</label>
        <div className="creator-list">
          {creators?.map(creator => (
            <div key={creator.id} className="creator-option">
              <input
                type="checkbox"
                checked={config.creators.includes(creator.id)}
                onChange={() => handleCreatorToggle(creator.id)}
              />
              <label>
                <strong>{creator.name}</strong>
                <span className="creator-meta">
                  Tier {creator.tier} • {creator.confidence}% confidence • {creator.successRate.toFixed(0)}% win rate
                </span>
              </label>
            </div>
          ))}
        </div>
      </div>

      {/* Symbol Allocation */}
      <div className="form-section">
        <label>Symbol Allocation</label>
        <div className="symbol-allocation">
          {['ETHE', 'GBTC', 'FXA'].map(symbol => (
            <div key={symbol} className="symbol-row">
              <label>{symbol}</label>
              <input
                type="range"
                min="0"
                max="100"
                value={(config.symbols[symbol] || 0) * 100}
                onChange={(e) => handleSymbolAllocation(symbol, parseInt(e.target.value))}
              />
              <span>{((config.symbols[symbol] || 0) * 100).toFixed(0)}%</span>
            </div>
          ))}
        </div>
        <div className="allocation-summary">
          Total: {Object.values(config.symbols).reduce((a, b) => a + b, 0) * 100}%
        </div>
      </div>

      {/* Entry/Exit Configuration */}
      <div className="form-section">
        <label>Entry & Exit Strategy</label>
        
        <div className="strategy-row">
          <label>Take Profit Target</label>
          <input
            type="number"
            step="0.01"
            min="0.01"
            max="0.5"
            value={config.takeProfit}
            onChange={(e) => setConfig({ ...config, takeProfit: parseFloat(e.target.value) })}
          />
          <span>{(config.takeProfit * 100).toFixed(1)}%</span>
        </div>

        <div className="strategy-row">
          <label>Stop Loss</label>
          <input
            type="number"
            step="0.01"
            min="-0.5"
            max="0"
            value={config.stopLoss}
            onChange={(e) => setConfig({ ...config, stopLoss: parseFloat(e.target.value) })}
          />
          <span>{(config.stopLoss * 100).toFixed(1)}%</span>
        </div>
      </div>

      {/* Deployment Configuration */}
      <div className="form-section">
        <label>Deployment Settings</label>
        
        <div className="deployment-row">
          <label>Batch Size (Total Orders)</label>
          <input
            type="number"
            min="10"
            max="500"
            value={config.batchSize}
            onChange={(e) => setConfig({ ...config, batchSize: parseInt(e.target.value) })}
          />
        </div>

        <div className="deployment-row">
          <label>Wave Interval (seconds)</label>
          <input
            type="number"
            min="30"
            max="300"
            step="10"
            value={config.waveInterval}
            onChange={(e) => setConfig({ ...config, waveInterval: parseInt(e.target.value) })}
          />
        </div>
      </div>

      {/* Preview & Deploy */}
      <div className="form-section preview">
        <h3>Deployment Preview</h3>
        <div className="preview-stats">
          <p>
            <strong>Creators:</strong> {config.creators.join(', ') || 'None'}
          </p>
          <p>
            <strong>Total Orders:</strong> {config.batchSize}
          </p>
          <p>
            <strong>Waves:</strong> {Math.ceil(config.batchSize / 10)} (90 seconds each)
          </p>
          <p>
            <strong>Expected Duration:</strong> {Math.ceil((config.batchSize / 10) * (config.waveInterval / 60))} minutes
          </p>
        </div>

        <button
          className="deploy-button"
          onClick={() => generateOrders.mutate(config)}
          disabled={generateOrders.isPending}
        >
          {generateOrders.isPending ? 'Generating Orders...' : 'Generate & Deploy'}
        </button>
      </div>

      {generateOrders.isError && (
        <div className="error">
          Error: {(generateOrders.error as Error).message}
        </div>
      )}

      {generateOrders.isSuccess && (
        <div className="success">
          ✅ Orders generated! Ready to deploy.
        </div>
      )}
    </div>
  );
};
