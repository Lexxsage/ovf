import kotlin.math.log
import kotlin.math.pow

fun main() {
    val floatEpsilon = findFloatEpsilon()
    val doubleEpsilon = findDoubleEpsilon()
    findEFloat()
    findEDouble()
    compareNumbersFloat(floatEpsilon)
    compareNumbersDouble(doubleEpsilon)
}

fun findFloatEpsilon(): Float{
    var epsilon = 1.0F
    var epsPrecision = 0

    while ( (1.0F + epsilon) != 1.0F ){
        epsilon /= 2.0F
        epsPrecision++
    }

    println("FLOAT - single precision")
    println("Epsilon = ${epsilon*2.0F}")
    println("Mantissa precision = ${epsPrecision - 1} bits")
    println("")
    return epsilon
}

fun findDoubleEpsilon():Double{
    var epsilon = 1.0
    var epsPrecision = 0

    while ( (1.0 + epsilon) != 1.0 ){
        epsilon /= 2.0
        epsPrecision++
    }
    println("DOUBLE - double precision")
    println("Epsilon = ${epsilon*2.0}")
    println("Mantissa precision = ${epsPrecision - 1} bits")
    println("")
    return epsilon
}

fun findEFloat() {
    var xCurrent = 1.0F
    var eMax = 0

    while (xCurrent != Float.POSITIVE_INFINITY) {
        xCurrent *= 2.0F
        eMax++
    }

    println("FLOAT E max and E min")
    println("E max = ${eMax - 1 }")

    val w = log(eMax.toDouble(), 2.0).plus(1.0)
    val eMin = (2.0.pow((w - 1))).toInt() - 2

    println("E min = $eMin")
    println("")
}

fun findEDouble(){
    var xCurrent = 1.0
    var eMax = 0

    while (xCurrent != Float.POSITIVE_INFINITY.toDouble()) {
        xCurrent *= 2.0
        eMax++
    }

    println("DOUBLE E max and E min")
    println("E max = ${eMax - 1 }")

    val w = log(eMax.toDouble(), 2.0).plus(1.0)
    val eMin = (2.0.pow((w - 1))).toInt() - 2

    println("E min = $eMin")
    println("")
}

fun compareNumbersFloat(epsilon: Float){
    val compareList = arrayListOf(
        1.0,
        1.00000000 + epsilon + epsilon/2,
        1.00000000 + epsilon/2,
        1.00000000 + epsilon
    )
    println("FLOAT compare")
    for ( i in 0..3){
        var j = i + 1
        while (j < 4){
            println("$i, $j")
            when{
                compareList.getOrNull(i)!! < compareList.getOrNull(j)!! -> println("${compareList.getOrNull(i)} less then ${compareList.getOrNull(j)}")
                compareList.getOrNull(i)!! > compareList.getOrNull(j)!! -> println("${compareList.getOrNull(i)} more then ${compareList.getOrNull(j)}")
                compareList.getOrNull(i)!! == compareList.getOrNull(j)!! -> println("${compareList.getOrNull(i)} equal ${compareList.getOrNull(j)}")
            }
            j++
        }
    }
    println("")
}

fun compareNumbersDouble(epsilon: Double){
    val compareList = arrayListOf(
        1.0,
        10.0.pow(-17) + epsilon + epsilon/2,
        10.0.pow(-17) + epsilon/2,
        10.0.pow(-17) + epsilon
    )
    println("DOUBLE compare")
    for ( i in 0..3){
        var j = i + 1
        while (j < 4){
            println("$i, $j")
            when{
                compareList.getOrNull(i)!! < compareList.getOrNull(j)!! -> println("${compareList.getOrNull(i)} less then ${compareList.getOrNull(j)}")
                compareList.getOrNull(i)!! > compareList.getOrNull(j)!! -> println("${compareList.getOrNull(i)} more then ${compareList.getOrNull(j)}")
                compareList.getOrNull(i)!! == compareList.getOrNull(j)!! -> println("${compareList.getOrNull(i)} equal ${compareList.getOrNull(j)}")
            }
            j++
        }
    }
    println("")
}