# Paytracker

**Paytracker** is a full-stack web application built with Django and Bootstrap that helps salespeople log, track, and analyze their commissions. It streamlines compensation tracking by replacing pen-and-paper methods with a centralized, dynamic, and user-friendly platform for recording sales and calculating commission-based earnings.
#### Video Demo:  https://youtu.be/qyknkRDPqS4

---

## Overview

Salespeople in high-paced environments often track their earnings manually, using ledgers or sticky notes. This approach is prone to loss, disorganization, and inefficiency. **Paytracker** was developed to address this issue by providing a digital platform that allows users to:

- Log sales with timestamps automatically recorded
- Define custom commission structures
- View dynamic earnings metrics
- Receive automatic calculations for bonuses, scaling commissions, and flat rates

The app is fully backed by a relational database and incorporates Django’s authentication system to ensure secure, user-specific data management.

---

## Features

### Core Functionality

- **Sales Logging**: Users can log individual sales, which are timestamped and tied to their account.
- **Commission Tracking**: The platform supports complex pay structures including:
    - **Scaling commission rates** (e.g., 20% base, increasing to 25% after 10 sales)
    - **Volume bonuses** (extra compensation upon reaching sales milestones)
    - **Flat-rate compensation** (fallback payout when commissions fall below a threshold)
- **Monthly Filters & Metrics**: Users can filter sales by month and view real-time analytics on performance and earnings.

---

## Data Models

- **Sale**: Tracks sales data, including amount, user, and timestamp.
- **Payplan**: Stores commission structures and thresholds.
- **VolumeBonus**: Captures milestone-based bonuses.
- **Flat**: Manages fallback compensation rules.
- **User**: Extends Django’s user model to include personalized account info.

All financial logic is dynamically calculated and accounts for changing plans, deleted entries, or evolving compensation terms.

---

## App Structure

Paytracker is divided into modular Django apps:

### `homepage`

- Static intro and user onboarding pages.
- Independent layout for future scalability.

### `payplan`

- Handles creation and modification of user-specific pay plans.
- Manages commission tiers, volume bonuses, and flat-rate setups.
- Views are designed to handle both `GET` (rendering forms) and `POST` (saving data) requests.

### `saletracker`

- Displays user dashboards with key sales metrics.
- Allows logging and deletion of individual sales.
- Dynamic logic reflects commission tiers, bonuses, and sales history accurately.

### `users`

- Manages authentication: login, logout, registration.
- Connects users to all other data via foreign keys.

---

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: Bootstrap (HTML, CSS)
- **Database**: SQLite (default, easily portable to PostgreSQL)
- **Authentication**: Django’s built-in auth system
- **Templating**: Django templates with isolated layouts per app
