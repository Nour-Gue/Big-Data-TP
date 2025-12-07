package spark.streaming.tp2;

import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Encoders;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.streaming.StreamingQuery;
import org.apache.spark.sql.streaming.StreamingQueryException;
import org.apache.spark.sql.streaming.Trigger;

import java.util.Arrays;
import java.util.concurrent.TimeoutException;

public class streamS {
    public static void main(String[] args) throws StreamingQueryException, TimeoutException {

        SparkSession spark = SparkSession.builder()
                                         .appName("NetworkWordCount")
                                         .master("local[*]")
                                         .getOrCreate();

        Dataset<String> lines = spark.readStream()
                                     .format("socket")
                                     .option("host", "localhost")
                                     .option("port", 9999)
                                     .load()
                                     .as(Encoders.STRING());

        Dataset<String> words = lines.flatMap(
            (String line) -> Arrays.asList(line.split(" ")).iterator(),
            Encoders.STRING()
        );

        Dataset<Row> wordCounts = words.groupBy("value").count();

        StreamingQuery query = wordCounts.writeStream()
                                         .outputMode("complete")
                                         .format("console")
                                         .trigger(Trigger.ProcessingTime("1 second"))
                                         .start();

        query.awaitTermination();
    }
}
