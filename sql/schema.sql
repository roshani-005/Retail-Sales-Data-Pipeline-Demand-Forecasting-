PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS material_master (
 material_id TEXT PRIMARY KEY, material_name TEXT NOT NULL, category TEXT NOT NULL,
 primary_supplier TEXT NOT NULL, unit_cost REAL NOT NULL, lead_time_days INTEGER NOT NULL,
 moq INTEGER NOT NULL, avg_daily_demand REAL NOT NULL, target_service_level REAL NOT NULL, criticality TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS supplier_master (supplier_id TEXT PRIMARY KEY, supplier_name TEXT NOT NULL, country TEXT, supplier_tier TEXT);
CREATE TABLE IF NOT EXISTS material_demand (date DATE NOT NULL, material_id TEXT NOT NULL, demand_qty INTEGER NOT NULL, demand_source TEXT NOT NULL,
 FOREIGN KEY(material_id) REFERENCES material_master(material_id));
CREATE TABLE IF NOT EXISTS purchase_orders (po_id TEXT PRIMARY KEY, material_id TEXT NOT NULL, supplier_id TEXT NOT NULL, due_date DATE NOT NULL, receipt_date DATE NOT NULL,
 ordered_qty INTEGER NOT NULL, received_qty INTEGER NOT NULL, rejected_qty INTEGER NOT NULL, unit_cost REAL NOT NULL,
 FOREIGN KEY(material_id) REFERENCES material_master(material_id), FOREIGN KEY(supplier_id) REFERENCES supplier_master(supplier_id));
CREATE TABLE IF NOT EXISTS inventory_snapshots (snapshot_date DATE NOT NULL, material_id TEXT NOT NULL, on_hand_qty INTEGER NOT NULL, reserved_qty INTEGER NOT NULL,
 FOREIGN KEY(material_id) REFERENCES material_master(material_id));
CREATE INDEX IF NOT EXISTS idx_demand_material_date ON material_demand(material_id,date);
CREATE INDEX IF NOT EXISTS idx_inventory_material_date ON inventory_snapshots(material_id,snapshot_date);
CREATE INDEX IF NOT EXISTS idx_po_material_due ON purchase_orders(material_id,due_date);
