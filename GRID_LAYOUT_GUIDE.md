# 🎯 Multi-Stream Grid Layout Guide

The multi-stream recorder now features **intelligent layout switching** that automatically uses a horizontal grid layout when monitoring many streams (like 20+ users). This makes it much more efficient to monitor large numbers of streams simultaneously.

## 🎨 **Layout Types**

### 📊 **Vertical Layout** (≤6 streams)
Perfect for monitoring a small number of streams with detailed information:

```
Stream-1: 🔴 Recording
  📺 @username1
  ⏱️  00:15:30 | 📁 25.3 MB | [████████████████████████████░░]

Stream-2: ⏳ Waiting
  📺 @username2  
  ⏱️  00:00:00 | 📁 0.0 MB | [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]
```

### 🎯 **Grid Layout** (>6 streams)
Efficient horizontal layout for monitoring many streams:

```
Stream-1 🔴 | @user1 | 00:15:30 | 25.3MB | [████████████████████░]
Stream-2 ⏳ | @user2 | 00:00:00 | 0.0MB  | [░░░░░░░░░░░░░░░░░░░░]
Stream-3 🔄 | @user3 | 00:02:45 | 5.1MB  | [██░░░░░░░░░░░░░░░░░░]
```

## 🚀 **Usage Examples**

### **Small Scale Monitoring** (Vertical Layout)
```bash
# Monitor 3-6 users (uses vertical layout)
python main.py -users user1 user2 user3 -mode automatic -automatic-interval 5
```

### **Large Scale Monitoring** (Grid Layout)  
```bash
# Monitor 20 users (automatically uses grid layout)
python main.py -users user1 user2 user3 user4 user5 user6 user7 user8 user9 user10 user11 user12 user13 user14 user15 user16 user17 user18 user19 user20 -mode automatic -automatic-interval 5

# Or using a file with usernames
python main.py -users $(cat usernames.txt) -mode automatic -automatic-interval 10
```

## 🎛️ **Grid Layout Features**

### **Automatic Layout Detection**
- **≤6 streams**: Detailed vertical layout
- **>6 streams**: Compact grid layout
- **Dynamic columns**: 2-4 columns based on terminal width
- **Responsive design**: Adapts to terminal size

### **Compact Information Display**
Each stream shows:
- **Stream ID**: `Stream-1`, `Stream-2`, etc.
- **Status Emoji**: ⏳ 🔄 🔴 ✅
- **Username**: `@username` (truncated to fit)
- **Duration**: `HH:MM:SS` format
- **File Size**: `XX.XMB`
- **Progress Bar**: Visual progress indicator

### **Status Indicators**
| Emoji | Status | Meaning |
|-------|--------|---------|
| ⏳ | Waiting | Monitoring user, waiting for them to go live |
| 🔄 | Starting | User went live, initializing recording |
| 🔴 | Recording | Actively recording the live stream |
| ✅ | Completed | Recording finished successfully |

## 📊 **Terminal Layout**

### **2-Column Layout** (Narrow terminals)
```
Stream-1 🔴 | @user1 | 00:15:30 | 25.3MB    Stream-2 ⏳ | @user2 | 00:00:00 | 0.0MB
Stream-3 🔄 | @user3 | 00:02:45 | 5.1MB     Stream-4 ✅ | @user4 | 00:45:12 | 67.8MB
```

### **3-Column Layout** (Medium terminals)  
```
Stream-1 🔴 | @user1 | 00:15:30    Stream-2 ⏳ | @user2 | 00:00:00    Stream-3 🔄 | @user3 | 00:02:45
Stream-4 ✅ | @user4 | 00:45:12    Stream-5 🔴 | @user5 | 00:12:30    Stream-6 ⏳ | @user6 | 00:00:00
```

### **4-Column Layout** (Wide terminals)
```
Stream-1 🔴 | @user1    Stream-2 ⏳ | @user2    Stream-3 🔄 | @user3    Stream-4 ✅ | @user4
Stream-5 🔴 | @user5    Stream-6 ⏳ | @user6    Stream-7 🔄 | @user7    Stream-8 ✅ | @user8
```

## 🎯 **Real-World Scenarios**

### **Content Creator Archive** (20+ streamers)
```bash
# Monitor popular TikTok creators
python main.py -users creator1 creator2 creator3 creator4 creator5 creator6 creator7 creator8 creator9 creator10 creator11 creator12 creator13 creator14 creator15 creator16 creator17 creator18 creator19 creator20 -mode automatic -automatic-interval 5
```

**Dashboard Preview:**
```
📊 Multi-Stream Recording Dashboard
┌─────────────────────────────────────────────────────────────┐

Stream-1 🔴 | @creator1   Stream-2 ⏳ | @creator2   Stream-3 🔄 | @creator3
Stream-4 ✅ | @creator4   Stream-5 🔴 | @creator5   Stream-6 ⏳ | @creator6
Stream-7 🔄 | @creator7   Stream-8 ✅ | @creator8   Stream-9 🔴 | @creator9
...

📊 Total: 20 | 🔴 Active: 8 | ✅ Completed: 3 | ⏳ Waiting: 9
└─────────────────────────────────────────────────────────────┘
```

### **Event Coverage** (Multiple concurrent streams)
```bash
# Monitor event with multiple angles/hosts
python main.py -users host1 host2 guest1 guest2 audience1 audience2 backstage official -mode automatic -automatic-interval 2
```

## 💡 **Tips & Best Practices**

### **For Large Scale Monitoring**
1. **Use wider terminals**: More columns = better overview
2. **Reasonable intervals**: 5-10 minutes for automatic mode
3. **Monitor resources**: 20+ streams use significant bandwidth/storage
4. **Group by priority**: Monitor most important streamers first

### **Terminal Optimization**
- **Minimum width**: 120 characters recommended for 3+ columns
- **Dark themes**: Colors show better on dark backgrounds  
- **Font size**: Smaller fonts allow more columns
- **Keep terminal open**: Dashboard updates in real-time

### **Performance Considerations**
- **Concurrent limit**: 20-30 streams max on most systems
- **Network bandwidth**: ~1-2 Mbps per active stream
- **Storage space**: Plan for ~50-100MB per hour per stream
- **CPU usage**: More streams = higher CPU usage

## 🔧 **Configuration**

### **Layout Threshold**
The system automatically switches layouts at 6 streams:
- **1-6 streams**: Vertical layout (detailed view)
- **7+ streams**: Grid layout (compact view)

### **Column Calculation**
```
terminal_width = get_terminal_width()
min_column_width = 35  # Minimum space needed per stream
max_columns = min(4, terminal_width // min_column_width)
columns_per_row = max(2, max_columns)
```

### **Responsive Behavior**
- **<70 chars**: 2 columns (minimum)
- **70-104 chars**: 2 columns  
- **105-139 chars**: 3 columns
- **140+ chars**: 4 columns (maximum)

## 🎭 **Demo & Testing**

### **Test Grid Layout**
```bash
cd src/
python3 quick_grid_test.py
```

### **Full Grid Demo**
```bash
cd src/  
python3 grid_layout_demo.py
```

## 🌟 **Benefits**

### **Efficiency**
- **Space optimization**: Monitor 20 streams in same screen space as 6
- **Quick overview**: See all stream statuses at a glance
- **Status recognition**: Emoji indicators for instant status understanding

### **Scalability** 
- **Handle many streams**: Perfect for 20+ concurrent recordings
- **Responsive design**: Adapts to any terminal size
- **Automatic switching**: No manual configuration needed

### **Professional Experience**
- **Clean interface**: Organized, easy to read layout
- **Real-time updates**: Live progress tracking
- **Visual consistency**: Maintains TikTok brand theme

---

## 🎯 **Summary**

The grid layout feature makes the multi-stream recorder **perfect for large-scale monitoring**:

- ✅ **Automatic layout switching** based on stream count
- ✅ **Horizontal grid** for efficient space usage  
- ✅ **2-4 responsive columns** based on terminal width
- ✅ **Compact stream information** with emoji status
- ✅ **Real-time progress tracking** for all streams
- ✅ **Professional dashboard** experience

**Perfect for monitoring 20+ TikTok streamers simultaneously!** 🚀
