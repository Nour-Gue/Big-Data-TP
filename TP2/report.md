# Big Data CSV Processing Report

This project evaluates three methods to process a large CSV file (~7.6 GB) containing **User Achievements** data. The goal is to compare  **performance** ,  **memory usage** , and  **compression benefits** .

## File Details

* **Path:** `C:\Users\LAPTA\Big-Data-TP\TP2\UserAchievements.csv`
* **Size:** 7631.82 MB (~7.6 GB)
* **Rows:** 107,099,252

---

## 1. **Pandas with Chunking**

**Method:** Reading the CSV in chunks of 100,000 rows.

<pre class="overflow-visible!" data-start="615" data-end="741"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>chunksize = </span><span>100_000</span><span>
chunks = pd.read_csv(path, chunksize=chunksize)
</span><span>for</span><span> chunk </span><span>in</span><span> chunks:
    count += </span><span>len</span><span>(chunk)
</span></span></code></div></div></pre>

**Results:**

* **Rows processed:** 107,099,252
* **Time:** 459.23 s
* **RAM Used:** 9.66 MB

**Pros:**

* Very low memory usage (good for machines with limited RAM).

**Cons:**

* Slower compared to Dask for very large files.

---

## 2. **Dask DataFrame**

**Method:** Using Dask for out-of-core parallel processing.

<pre class="overflow-visible!" data-start="1079" data-end="1191"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>import</span><span> dask.dataframe </span><span>as</span><span> dd
df_dask = dd.read_csv(csv_file)
row_count = df_dask.shape[</span><span>0</span><span>].compute()
</span></span></code></div></div></pre>

**Results:**

* **Rows processed:** 107,099,252
* **Time:** 99.16 s
* **RAM Used:** 127.78 MB

**Pros:**

* Fast reading and processing.
* Can handle datasets larger than memory.

**Cons:**

* Higher memory consumption than Pandas chunking.

---

## 3. **CSV Compression (gzip)**

**Method:** Compressing CSV to reduce storage space.

<pre class="overflow-visible!" data-start="1546" data-end="1699"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>import</span><span> gzip, shutil
</span><span>with</span><span></span><span>open</span><span>(src_path, </span><span>'rb'</span><span>) </span><span>as</span><span> f_in:
    </span><span>with</span><span> gzip.</span><span>open</span><span>(dst_path, </span><span>'wb'</span><span>) </span><span>as</span><span> f_out:
        shutil.copyfileobj(f_in, f_out)
</span></span></code></div></div></pre>

**Results:**

* **Original Size:** 7631.82 MB
* **Compressed Size:** 521.14 MB (~93% reduction)
* **Time:** 2260.12 s

**Pros:**

* Significant storage saving.
* Can speed up future reading with `compression='gzip'` in Pandas/Dask.

**Cons:**

* Compression is time-consuming.
* Requires decompression for some operations.

---

## Conclusion

| Method          | Time (s) | RAM Used (MB) | Notes                               |
| --------------- | -------- | ------------- | ----------------------------------- |
| Pandas Chunking | 459.23   | 9.66          | Very memory-efficient, slower       |
| Dask DataFrame  | 99.16    | 127.78        | Fastest, moderate memory usage      |
| CSV Compression | 2260.12  | N/A           | Great for storage, slow to compress |

**Best method for processing:**  **Dask** , due to speed and ability to handle very large datasets efficiently.

**Best method for storage:**  **Compression (gzip)** , reduces file size drastically.
