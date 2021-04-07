# 基于Content-Base、Collaborative Filtering及Logistic Regression算法的推荐系统Demo实现

# 1.结论

## 项目背景

基于目前生活中，我们常见的抖音、快手、今日头条等高日活APP，都应用了数据挖掘算法实现的推荐系统。在此，我们希望可以应用网上下载的数据集，搭建一个推荐系统模拟demo。本项目应用的是音乐数据集，包含用户画像数据、用户行为数据以及物品元数据（音乐的相关数据，如播放时长等）。

我们的想法是：

a. 基于用户历史数据，我们通过内容相似度算法和协同过滤算法分别计算每首歌曲两两之间的相似度，形成每首歌曲对应与多首歌曲相似的数据结构；

b. 假设我们想看与某首歌曲相似的100首歌曲，即可通过该数据结构提取数据，得到一个与该歌曲相似的100首歌曲列表；

c. 同时，通过历史数据，应用逻辑回归算法挖掘用户对某首歌曲的喜好程度，得到用户对歌曲的喜好值；

d. 之后对相似的100首歌曲根据逻辑回归算法进行降序排序，从而得到最佳推荐的10首歌曲推荐给用户。

## CB算法推荐

在CB算法计算两两歌曲之间的相似度算法中，首先得到共135239532条ItemA-ItemB-Score数据；之后将数据整合，得到与ItemA相似的歌曲列表，共45940条这样的歌曲列表（每个Item对应一个列表）。这里的Item指的是歌曲，Score代表相似度，后续不再赘述。

## CF算法推荐

同样，在CF算法计算两两歌曲之间的相似度算法中，首先得到共2568542条ItemA-ItemB-Score数据；之后将数据整合，得到与ItemA相似的歌曲列表，共39963条这样的歌曲列表（每个Item对应一个列表）。

## LR算法精排

在LR算法中，首先构建模型，得到用户对歌曲的喜好模型（参数W和B），共29331个模型特征，因此得到29331个W参数，以及一个B参数

## 模拟Demo实现

最后，模拟Demo实现过程：

* 用户输入用户ID以及物品ID
* 返回用户最可能喜欢的10首歌曲

# 2.项目概述

![image-20210318110915888](F:\mygit\recommender\基于Content-Base、Collaborative Filtering及Logistic Regression算法的推荐系统Demo实现.assets\image-20210318110915888.png)

## 算法应用原理

### 基于内容相似度的算法推荐

总结CB算法的原理，其实归结于一句话：根据用户历史喜欢的内容为他推荐喜欢的内容的相似内容。CB算法全称---Content Base，即基于内容，进行两物品的相似度计算。

方法：从非结构化数据提取表征，计算相应的表征值，从而形成结构化数据。再分类算法，基于历史数据（用户喜欢的内容或者不喜欢的内容）训练分类器，最终得到一组用户最喜欢的Item进行推荐。

步骤：

第一步：内容表征。从非结构化数据中提取表征，以一篇文章为例，提取文章中的分词作为表征，并计算每个分词的TF-IDF值，从而得到(ItemID, substring1:value, substring2:value…)类似结构的数据；

第二步：特征学习。假设用户已经对一些item做了喜好判断，喜欢其中的一部分，不喜欢其中的另外一部分。从这些数据，我们可以构建，训练并得到一个喜好分类器。给定一个新的item通过分类器判断喜好，最终形成“喜”的item列表，并根据喜好程度值进行降序；(最常用的是朴素贝叶斯算法，其次是K近邻，决策树)

第三步：生成推荐列表。根据第二步得到的item列表，抽取用户最喜欢的topN个项目作为返回。

在本项目中，我们应用CB算法第一步，得到(ItemID, substring1:value, substring2:value…)类似结构的数据；之后进行所有数据的整合，得到[(Itemi, substringk, value), (Itemo ,substringp, value)…]的数据结构；对于具有同一个substring的ItemID，认为这些ItemID具有相似性，因此下一步计算ItemA与ItemB的相似度，从而得到类似[(ItemA, ItemB, Score)…]的数据结构；而对于每个ItemA，可以看到有多个与之相似的ItemB，从而我们容易与ItemA相似的Item列表。

![image-20210318111009171](F:\mygit\recommender\基于Content-Base、Collaborative Filtering及Logistic Regression算法的推荐系统Demo实现.assets\image-20210318111009171.png)

对于CF算法（Collaborative Filterin，协同过滤算法）而言，我们存在两种形式。一种是基于用户的协同过滤算法，另一种是基于物品的协同过滤算法。

下面具体展开看这两种算法：

### 基于用户的协同过滤算法

目标：当一个用户A需要个性化推荐的时候， 我们可以先找到和他有相似兴趣的其他用户， 然后把那些用户喜欢的， 而用户A没有听说过的物品推荐给A

方法：利用用户对多个物品的打分数值（用户的打分向量），计算用户相似度，排序得到topN的用户相似集合；找到用户相似集合中用户喜欢的但是目标用户（即用户A）没有听说过的物品集合，进行推荐度计算，排序，形成topN推荐度的物品集合，推荐给目标用户。

步骤：

第一步，计算用户相似度。这里需要用到用户的打分向量进行相似度计算。相似度的度量可以是余弦相似度或者皮尔逊相关系数；

1， 余弦相似度：

​              														![image-20210318111612292](F:\mygit\recommender\基于Content-Base、Collaborative Filtering及Logistic Regression算法的推荐系统Demo实现.assets\image-20210318111612292.png)

2， 皮尔逊相关系数：

![image-20210318111541070](F:\mygit\recommender\基于Content-Base、Collaborative Filtering及Logistic Regression算法的推荐系统Demo实现.assets\image-20210318111541070.png)

​                       

第二步：根据第一步计算而得的用户相似度进行降序排序，得到前TopN个高相关用户集合，找到这些用户喜欢但是目标用户还不知道的物品，进行推荐度计算。

物品推荐度公式：

​																![image-20210318111625940](F:\mygit\recommender\基于Content-Base、Collaborative Filtering及Logistic Regression算法的推荐系统Demo实现.assets\image-20210318111625940.png)

这条公式的含义是：目标用户的历史评分均值+相似用户对该物品的评分与此用户的历史评分均值的差值进行相似度加权平均。其中，![img](file:///C:/Users/DELL/AppData/Local/Temp/msohtmlclip1/01/clip_image002.png)表示用户i（即目标用户）对目标物品j的评分，k表示相似用户的序数，![img](file:///C:/Users/DELL/AppData/Local/Temp/msohtmlclip1/01/clip_image004.png)表示用户i与用户k的相似度，![img](file:///C:/Users/DELL/AppData/Local/Temp/msohtmlclip1/01/clip_image006.png)表示相似用户对目标物品的评分。

### 基于物品的协同过滤算法

目标：当一个用户A需要个性化推荐的时候， 我们可以先找到与用户喜欢的物品相似的相似物品， 然后把它推荐给A

方法：利用物品本身的多个用户的打分数值（物品的用户打分向量），计算物品相似度，排序得到topN的物品相似集合；再根据目标用户（即用户A）对相似物品的打分，进行目标物品的推荐度计算，排序，形成topN推荐度的物品集合，推荐给目标用户。

物品推荐度公式：

​																![image-20210318111723286](F:\mygit\recommender\基于Content-Base、Collaborative Filtering及Logistic Regression算法的推荐系统Demo实现.assets\image-20210318111723286.png)

这条公式的含义是：目标物品的历史评分均值+目标用户对相似物品的评分与此物品的历史评分均值的差值进行相似度加权平均。其中，![img](file:///C:/Users/DELL/AppData/Local/Temp/msohtmlclip1/01/clip_image002.png)表示用户i（即目标用户）对目标物品j的评分，k表示相似物品的序数，![img](file:///C:/Users/DELL/AppData/Local/Temp/msohtmlclip1/01/clip_image004.png)表示物品i与物品k的相似度，![img](file:///C:/Users/DELL/AppData/Local/Temp/msohtmlclip1/01/clip_image006.png)表示目标用户对相似物品的评分。

在本项目中，我们应用的是基于物品的协同过滤算法。通过数据整合与计算，得到类似[(ItemA, ItemB, Score)…]的数据结构；而对于每个ItemA，可以看到有多个与之相似的ItemB，从而我们容易与ItemA相似的Item列表。

## 系统实现依赖环境

1, Python-Sklearn：LR模型构建与参数计算

2, Redis：数据缓存

3, Python-Web：Demo实现

# 3.Demo功能

用户登录账号，抓取用户ID

用户输入搜索曲目，抓取ItemID

返回离线推荐列表

# 4.技术实现过程

### 数据预处理-合并

原始数据存在三个表（源文件没有字段标识），分别是用户画像数据，用户行为数据以及物品元数据：

**用户画像数据**

| Userid | Gender | Age  | Salary | location |
| ------ | ------ | ---- | ------ | -------- |
| 用户ID | 性别   | 年龄 | 薪资   | 地域     |

 

**用户行为数据**

| Userid | Itemid | User_watch_timelen | Click_timelen |
| ------ | ------ | ------------------ | ------------- |
| 用户ID | 音乐ID | 用户收听时长       | 点击时长      |

 

**音乐元数据**

| Itemid | Name     | Desc | Total_lentime | Location | tags |
| ------ | -------- | ---- | ------------- | -------- | ---- |
| 音乐ID | 音乐名称 | 内容 | 音乐长度      | 产地     | 标签 |

 将上述三个文件写入merge_base.data文件并输出。

### CB算法数据准备及其实现

首先，抽取Name、Desc、以及Tags字段，分别用进行分词得到分词token。接着，针对三个字段，每个字段赋予相应的token权重值，用得分与权重值的乘积进行加权求和最终得到每个token对应每个Itemid的综合得分（数据文件cb_train.data，数据条382221）。

**cb_train.data**

|   Token    |  Itemid   | score |
| :--------: | :-------: | :---: |
| 例子：爱情 | 429759835 |  11   |

数据表中，score表示itemid的各个token在该Item中的重要程度。

3rd_CB2-1_token2Item_ScoreCal_cbTrain1.py

为了得到同一Token下的所有Item，首先需要经历**map阶段**（也就是map排序，对Token进行排序）,得到cb_train1.data，数据条382221

4th_CB2-2_Item2Item_ScoreCal_cbResult.py

得到按照Token进行排序的数据文件之后，我们进行两两Item之间相似度的计算。这里我们相似度的计算直接以两个Item的Score相乘得到相似度。这就是如下的**Reduce阶段**。

步骤：

1， 遍历数据条，判断每一条的Token是否与上一条的Token相同；若相同，则把相同Token的Item放进列表item_score_list内；若不相同，则开始进行item_score_list内所有元素的两两匹配，将两两Item的Score进行相乘得到该对Item的相似度Score1，写进文件内；

由于对于不同的Token，Item-a与Item-b配对得到一个组合，该组合可能出现多次（即该配对在同一Token内出现，但是也可能在另外的Token里出现），所以最终得到的Item-a_Item-b_score并不是唯一的。此时我们可以理解为，不同的Token对于同一配对都有相似度，下一个出现的Token对该组合的相似度进行了强化，所以遇到重复出现的配对，我们对他们的Score进行相加，最终得到不重复出现的Item-a_Item-b_score组合，输出到文件中，（数据文件cb_result，数据条数135239532）。第二步到此结束。

### 组合数据

5th_CB3_Item2[Item-Score]_groupCal_cbReclis.py

上一步得到数据结构如Item-a_Item-b_score的数据，要知道，对于这样的结构，其中Item-a对应的Item-b_score不止一个，所以对于相同的Item-a要把所有的Item-i_score组合在一个列表中，方便调用，最终得到形如Item-a[Item-i_score]的数据结构。数据文件cb_reclist.redis，数据条数45940。

### 将组合数据导入Redis库

6th_cbReclist_to_RedisSQL.py

### CF算法数据准备及其实现

1， 计算组合user-item的score

1st_CF1_User2Item_ScoreCal_cfTrain.py

同一User下两两Item之间的相似度如何度量呢？一般考虑直接相乘得到。但是又如何度量User对某一Item的得分呢？这里我们用用户的观看时长除以总时长得到该用户对该Item的得分。所以，首先从数据文件Mer_base.data文件中提取四个指标，User, Item, User_watch_timelen以及Total_lentime四个指标；然后，对于同一组合User-Item的所有User_watch_timelen进行合并相加，Total_lentime也做同样的处理；再针对组合User-Item的sum(User_watch_timelen)和sum(Total_lentime)相除得到score

2， 对score进行单位化计算

2rd_CF2-1_Item[Sorted]2User_ScoreCal_cfTrain1.py

3th_CF2-2_0_User2Item_ScoreNormalize_cfTrain2.py

由于score指标属于Item指标（按照ItemCF的思想），所以需要统计每个Item的得分向量（有很多User评分，所以形成一个向量），因此需要先对Item进行map排序，得到item_user_score, 通过计算（score1, score2, …）的模，对每一个score进行单位化。输出数据格式user_item_score(单位化后的score), 输出数据文件cf_train2.data，数据条数247999。

3， 计算同一User下的两联Item之间的相似度

3th_CF2-2_1_User[Sorted]2Item_ScoreCal_cfTrain3.py

4th_CF2-3_Item2Item_ScoreCal_cfResult.py

这一步类似cb（事实上整个CF过程雷同CB过程）

首先处理得到按照User进行排序的数据文件，之后我们进行两两Item之间相似度的计算。这里我们相似度的计算直接以两个Item的Score相乘得到相似度。这就是如下的Reduce阶段。

步骤：

1，  遍历数据条，判断每一条的User是否与上一条的User相同；若相同，则把相同User的Item放进列表item_score_list内；若不相同，则开始进行item_score_list内所有元素的两两匹配，将两两Item的Score进行相乘得到该对Item的相似度Score1，写进文件内；

2， 由于对于不同的User，Item-a与Item-b配对得到一个组合，该组合可能出现多次（即该配对在同一Token内出现，但是也可能在另外的Token里出现），所以最终得到的Item-a_Item-b_score并不是唯一的。此时我们可以理解为，不同的User对于同一配对都有相似度，下一个出现的User对该组合的相似度进行了强化，所以遇到重复出现的配对，我们对他们的Score进行相加，最终得到不重复出现的Item-a_Item-b_score组合，输出到文件中，（数据文件cf_result，数据条数2568542）。第二步到此结束。

### 组合数据

5th_CF3_Item2[Item-Score]_groupCal_cfReclis.py

上一步得到数据结构如Item-a_Item-b_score的数据，要知道，对于这样的结构，其中Item-a对应的Item-b_score不止一个，所以对于相同的Item-a要把所有的Item-i_score组合在一个列表中，方便调用，最终得到形如Item-a[Item-i_score]的数据结构。数据文件cb_reclist.redis，数据条数39963。

### 将组合数据导入Redis库

6th_cfReclist_to_RedisSQL.py

### LR算法数据准备及其实现

首先看Label的构建。逻辑回归label的构建以watch_time/total_time为基础，如果该值大于等于0.82，则设定为1；如果该值小于等于0.3，则设定为0.对于其他的情况则不考虑。即只取Label大于等于0.82和小于等于0.3的样本进行模型训练。

其次看数据指标的转换。先看用户特征，包括年龄以及性别，这些不好体现为0/1类型的数据，于是我们将性别分为两类，分别记为0（女）和1（男）（类别作为字段，值1设置为。比如一个男人，则他的性别表示为（0：0，1：1）；一个女人，则他的性别表示为为（0：1，1：0）），年龄类似，分别记为2，3，4，…；对于物品特征的token做同样的处理，所以最终形成的向量为行数（样本数量），列（类别，接近3W列）

由上述得到的数据进行训练集和测试集的划分，最终得到模型参数w和b，其中w的维度数目与类别的维度数目相对应，b值只有一个。

### 模拟Demo

利用web.py框架进行模型部署，输入为请求用户id以及请求物品id，输出为物品id，推荐物品id，对应的相似度（从高到低降序排列-Reverse=True）
