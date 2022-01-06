# PredictStarNumber
[RankedMapData](https://github.com/rakkyo150/RankedMapData)のデータをもとに、BeatSaverで公開されている譜面のScoreSaberのランク基準の星の数を予測するアプリ。<br>
[こちら](https://predictstarnumber.herokuapp.com/)から使えます。<br>
[PredictStarNumberHelper](https://github.com/rakkyo150/PredictStarNumberHelper)のモデルを使用。<br>
BeatSaverのAPIから取得できる情報のみで学習を行ったので、譜面にもよりますが、結構外れた値がでることもあります。<br>
なお、学習精度に関しては[PredictStarNumberHelper](https://github.com/rakkyo150/PredictStarNumberHelper)のmodelScore.jsonで確認できます。<br>
ちなみに、2022/1/3現在の精度は、trainScoreが0.9745135905035479、testScoreが0.9405029861621208です。
