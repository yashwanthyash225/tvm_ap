/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

/*!
 * \file tvm/arith/pattern.h
 * \brief Expression pattern detectors.
 */
#ifndef TVM_ARITH_PATTERN_H_
#define TVM_ARITH_PATTERN_H_

#include <tvm/ir/expr.h>
#include <tvm/tir/expr.h>

namespace tvm {
namespace arith {
/*!
 * \brief Detect if e can be rewritten as e = sum_{i=0}^{n-1} var[i] * coeff[i] + coeff[n]
 *  Where coeff[i] and base are invariant of var[j] for all i and j.
 *
 * \param e The expression to be detected.
 * \param vars List of variables to be used in detection.
 * \return [coeff[i]] if it is possible, empty array if it is not.
 */
Array<PrimExpr> DetectLinearEquation(const PrimExpr& e, const Array<tir::Var>& vars);

/*!
 * \brief Detect if expression corresponds to clip bound of the vars
 *
 * \param e The expression to be detected.
 * \param vars List of variables to be used in detection.
 * \return concat([min_value[i], max_value[i]]), None is returned if there is no min or max value
 *          return empty if the e does not match the pattern.
 */
Array<PrimExpr> DetectClipBound(const PrimExpr& e, const Array<tir::Var>& vars);

}  // namespace arith
}  // namespace tvm
#endif  // TVM_ARITH_PATTERN_H_
